from fastapi import HTTPException,status

class AppException(Exception):
    """Base exception for application errors."""
    pass

class InvalidCredentialsError(AppException):
    """Raised when authentication credentials are invalid."""
    pass

class MissingCredentialsError(AppException):
    """Raised when required authentication credentials are missing."""
    pass
    HTTPException(
        detail="Missing credentials. Enter either email or phone.",
        status_code=status.HTTP_400_BAD_REQUEST
        )

class KeyNotFoundError(AppException):
    """Raised when the api key was not found in db."""
    pass

class UnauthorizedKeyError(AppException):
    """Raised when a api key does not belong to current user."""
    pass

class InactiveKeyError(AppException):
    """raised when api key used to inspect is inactive."""
    pass

class LogNotFoundError(AppException):
    """Raised when the api key was not found in db."""
    pass

class UnauthorizedLogError(AppException):
    """Raised when a api key does not belong to current user."""
    pass

class MissingTokenError(AppException):
    """Raised when the token is missing."""
    pass

class AccessTokenError(AppException):
    """Raised when the token is not access type."""
    pass

class InvalidExpiredTokenError(AppException):
    """Raised when the token is invalid or expired."""
    pass

class UserAlreadyExistsError(AppException):
    """Raised when a user record already exists."""
    pass
    HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Another User already exists."
        )

class UserNotFoundError(AppException):
    """Raised when user was not found in db."""
    pass

class MissingLLMError(AppException):
    """Raised when the llm credentials is missing."""
    pass
