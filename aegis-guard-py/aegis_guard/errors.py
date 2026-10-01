class AegisError(Exception):
    """Base exception for the Aegis SDK."""
    status_code: int = 500
    detail: str = "Unexpected Aegis error occurred."
    def __init__(
        self,
        detail: str|None=None,
        status_code: int | None = None,
    ):
        if detail:
          self.detail = detail
        if status_code is not None:
          self.status_code = status_code
        super().__init__(self.detail)

class AegisAuthenticationError(AegisError):
    """Raised when the API key is invalid or unauthorized."""
    status_code=401


class AegisRateLimitError(AegisError):
    """Raised when the request is rate limited."""
    status_code=429

class AegisGatewayError(AegisError):
    """Raised when the upstream LLM or Aegis gateway fails."""
    status_code=502