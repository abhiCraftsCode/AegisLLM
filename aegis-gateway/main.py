import time
import hashlib
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.core.config import settings
from app.db import engine, Base, get_db
from app.schemas import InspectRequest,InspectResponse
from app.models import APIKey, AuditLog
from app.middleware.auth import verify_api_key
from app.middleware.rate_limiter import limiter
from app.engine.tier1 import scan_heuristics
from app.engine.tier2 import onnx_engine

# Lifespan context manager to auto-create DB tables on server startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Aegis Gateway starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("[INFO] Aegis Gateway shutting down...")
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Routes ---

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "onnx_model_loaded": onnx_engine.session is not None
    }

@app.post("/inspect", response_model=InspectResponse)
async def inspect_prompt(
    payload: InspectRequest,
    request: Request,
    api_key: APIKey = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyzes a prompt for prompt injection & security threats using Tier 1 and Tier 2 engines.
    """
    start_time = time.perf_counter()
    prompt = payload.prompt.strip()

    # Step 1: Tier 1 Heuristics Regex Scan
    is_threat, score, tier_triggered = scan_heuristics(prompt)

    # Step 2: Tier 2 DeBERTa ONNX Neural Scan (only if Tier 1 passed)
    if not is_threat:
        is_threat, score = onnx_engine.predict(prompt)
        if is_threat:
            tier_triggered = "TIER_2_DEBERTA_ONNX"

    action = "BLOCKED" if is_threat else "ALLOWED"
    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

    # Step 3: Log Privacy-Safe Audit Metrics (Zero Full Raw Text)
    prompt_hash = hashlib.sha256(prompt.encode('utf-8')).hexdigest()
    prompt_preview = prompt[:40]

    audit_entry = AuditLog(
        api_key_id=api_key.id,
        prompt_hash=prompt_hash,
        prompt_preview=prompt_preview,
        action=action,
        tier_triggered=tier_triggered,
        threat_score=score,
        latency_ms=latency_ms
    )
    db.add(audit_entry)
    await db.commit()

    return InspectResponse(
        is_threat=is_threat,
        threat_score=score,
        action=action,
        tier_triggered=tier_triggered,
        latency_ms=latency_ms
    )

@app.post("/chat/completions")
async def proxy_chat_completion(
    payload: ChatCompletionRequest,
    request: Request,
    api_key: APIKey = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    Pass-through proxy that inspects incoming user prompt before forwarding to upstream LLM providers.
    """
    # Extract last user message prompt
    user_prompts = [msg.get("content", "") for msg in payload.messages if msg.get("role") == "user"]
    combined_prompt = " ".join(user_prompts)

    if combined_prompt:
        # Run inspection pipeline
        inspect_req = InspectRequest(prompt=combined_prompt)
        inspection = await inspect_prompt(inspect_req, request, api_key, db)
        
        if inspection.is_threat:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Security Threat Detected",
                    "action": "BLOCKED",
                    "reason": f"Prompt injection threat blocked by {inspection.tier_triggered}",
                    "threat_score": inspection.threat_score
                }
            )

    # Forward request to upstream LLM API if clean
    if not payload.upstream_url:
        raise HTTPException(status_code=400, detail="An upstream_url must be provided.")
    target_url = payload.upstream_url
    forward_headers = {k: v for k, v in request.headers.items() if k.lower() not in ["host", "content-length"]}

    async with httpx.AsyncClient() as client:
        try:
            upstream_response = await client.post(
                target_url,
                json=payload.model_dump(exclude={"upstream_url"}),
                headers=forward_headers,
                timeout=30.0
            )
            return Response(
                content=upstream_response.content,
                status_code=upstream_response.status_code,
                headers=dict(upstream_response.headers)
            )
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Failed to reach upstream LLM provider: {str(e)}")