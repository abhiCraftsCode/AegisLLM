from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings

def get_api_key_identifier(request: Request) -> str:
    """
    Extracts rate limit identifier:
    Uses authenticated API Key ID if present, otherwise falls back to client IP.
    """
    if hasattr(request.state, "api_key") and request.state.api_key:
        return f"key:{request.state.api_key.id}"
    return get_remote_address(request)

# Global Limiter Instance using in-memory token bucket
limiter = Limiter(
    key_func=get_api_key_identifier,
    default_limits=[f"{settings.DEFAULT_RATE_LIMIT_RPM}/minute"]
)