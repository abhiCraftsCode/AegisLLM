from fastapi import HTTPException,status

class AppException(Exception):
    """Base exception for application errors."""

class InvalidCredentialsError(AppException):
    """Raised when authentication credentials are invalid."""

class MissingCredentialsError(AppException):
    """Raised when required authentication credentials are missing."""
    HTTPException(
        detail="Missing credentials. Enter either email or phone.",
        status_code=status.HTTP_400_BAD_REQUEST
        )

class KeyNotFoundError(AppException):
    """Raised when the api key was not found in db."""

class UnauthorizedKeyError(AppException):
    """Raised when a api key does not belong to current user."""

class InactiveKeyError(AppException):
    """raised when api key used to inspect is inactive."""

class LogNotFoundError(AppException):
    """Raised when the api key was not found in db."""

class UnauthorizedLogError(AppException):
    """Raised when a api key does not belong to current user."""

class MissingTokenError(AppException):
    """Raised when the token is missing."""

class AccessTokenError(AppException):
    """Raised when the token is not access type."""

class InvalidExpiredTokenError(AppException):
    """Raised when the token is invalid or expired."""

class UserAlreadyExistsError(AppException):
    """Raised when a user record already exists."""
    HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Another User already exists."
        )

class UserNotFoundError(AppException):
    """Raised when user was not found in db."""
