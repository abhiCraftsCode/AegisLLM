import time
from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.heuristics import scan_heuristics
from services.inference import AegisInferencePipeline, ThreatResult

pipeline: Optional[AegisInferencePipeline] = None
audit_logs = []

# Valid development key
VALID_KEYS = {"aegis_sec_9832749823": "Dev Account"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipeline
    pipeline = AegisInferencePipeline("aegis_model.onnx")
    yield
    print("Shutting down Aegis Gateway...")

app = FastAPI(title="AegisLLM Security Gateway", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_pipeline():
    return pipeline

@app.post("/v1/chat/completions")
async def security_proxy(
    request: Request, 
    ml_pipe: AegisInferencePipeline = Depends(get_pipeline)
):
    # 1. API Key Auth
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "").strip()
    if token not in VALID_KEYS:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid Aegis API Key.")

    payload = await request.json()
    messages = payload.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="Missing 'messages' array in payload.")

    user_prompt = messages[-1].get("content", "")

    # 2. Tier 1: Regex & PII Scanning
    heuristic_alert = scan_heuristics(user_prompt)
    if heuristic_alert:
        audit_logs.insert(0, {
            "timestamp": time.strftime("%H:%M:%S"),
            "prompt": user_prompt,
            "threat_score": 1.0,
            "action": heuristic_alert,
            "latency": "0.5ms"
        })
        return JSONResponse(
            status_code=403,
            content={"status": "BLOCKED", "threat_score": 1.0, "reason": heuristic_alert}
        )

    # 3. Tier 2: ONNX Model Inference (<15ms)
    result = ml_pipe.predict(user_prompt)

    if result.is_malicious:
        audit_logs.insert(0, {
            "timestamp": time.strftime("%H:%M:%S"),
            "prompt": user_prompt,
            "threat_score": result.threat_score,
            "action": "BLOCKED_ML",
            "latency": f"{result.latency_ms}ms"
        })
        return JSONResponse(
            status_code=403,
            content={"status": "BLOCKED", "threat_score": result.threat_score, "reason": "Adversarial prompt injection detected."}
        )

    # 4. Tier 3: Clean Prompt Forwarding
    audit_logs.insert(0, {
        "timestamp": time.strftime("%H:%M:%S"),
        "prompt": user_prompt,
        "threat_score": result.threat_score,
        "action": "ALLOWED",
        "latency": f"{result.latency_ms}ms"
    })

    return {
        "id": "chatcmpl-aegis-proxy",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": payload.get("model", "gpt-4o"),
        "choices": [{
            "message": {
                "role": "assistant",
                "content": f"[Aegis Verified Safe] Mock LLM response for: '{user_prompt}'"
            }
        }]
    }

@app.get("/v1/audit/logs")
async def fetch_audit_logs():
    return {"total": len(audit_logs), "logs": audit_logs}