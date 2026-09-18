from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """Base exception for application errors."""
    status_code: int = 500
    detail: str = "Unexpected application error occurred."

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail
        super().__init__(self.detail)


# --- Auth & User Exceptions ---
class InvalidCredentialsError(AppException):
    status_code = 401
    detail = "Invalid credentials."

class MissingCredentialsError(AppException):
    status_code = 400
    detail = "Missing credentials. Enter either email or phone."

class MissingTokenError(AppException):
    status_code = 401
    detail = "Authentication token is missing."

class AccessTokenError(AppException):
    status_code = 401
    detail = "Invalid token type."

class InvalidExpiredTokenError(AppException):
    status_code = 401
    detail = "Invalid or expired token."

class UserAlreadyExistsError(AppException):
    status_code = 409
    detail = "Another user already exists."

class UserNotFoundError(AppException):
    status_code = 404
    detail = "User not found."


# --- API Key Exceptions ---
class KeyNotFoundError(AppException):
    status_code = 404
    detail = "API key not found."

class UnauthorizedKeyError(AppException):
    status_code = 403
    detail = "You are not authorized to access this API key."

class InactiveKeyError(AppException):
    status_code = 401
    detail = "API key is inactive."

class InvalidKeyError(AppException):
    status_code = 401
    detail = "Invalid API key."


# --- Audit Log Exceptions ---
class LogNotFoundError(AppException):
    status_code = 404
    detail = "Audit log not found."

class UnauthorizedLogError(AppException):
    status_code = 403
    detail = "You are not authorized to access this audit log."


# --- Gateway & Upstream LLM Exceptions ---
class LLMCredentialsError(AppException):
    status_code = 400
    detail = "LLM configuration is missing from this API key."

# --- Onnx Model Exceptions ---
class ModelNotFoundError(AppException):
    status_code = 503
    detail = "Service Down. Search Engine Failure."

# --- Universal Clean Handler ---
async def exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )