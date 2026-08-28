import hashlib
from typing import Optional
from fastapi import Request, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import APIKey

security = HTTPBearer(auto_error=False)

def hash_api_key(raw_key: str) -> str:
    """Computes SHA-256 hash of raw API key for secure DB lookup."""
    return hashlib.sha256(raw_key.strip().encode('utf-8')).hexdigest()

async def verify_api_key(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    db: AsyncSession = Depends(get_db)
) -> APIKey:
    """
    Authenticates requests via Bearer token or 'X-API-Key' header.
    Validates key existence & active state in the database.
    """
    raw_key: Optional[str] = None

    # 1. Extract from Authorization Bearer header
    if credentials and credentials.credentials:
        raw_key = credentials.credentials
    # 2. Fallback to X-API-Key custom header
    elif "x-api-key" in request.headers:
        raw_key = request.headers.get("x-api-key")

    if not raw_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API Key. Provide key via Bearer token or 'X-API-Key' header."
        )

    # 3. Hash key and search DB
    key_hash = hash_api_key(raw_key)
    result = await db.execute(select(APIKey).where(APIKey.key_hash == key_hash))
    api_key_record = result.scalars().first()

    if not api_key_record or not api_key_record.is_active:
        raise HTTPException(
            status_code=403,
            detail="Invalid or revoked API Key."
        )

    # Attach key record to request state for downstream rate limiting and audit logging
    request.state.api_key = api_key_record
    return api_key_record