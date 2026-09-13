from fastapi import HTTPException,status

class AppException(Exception):
    """Base exception for application errors."""

class InvalidCredentialsError(AppException):
    """Raised when authentication credentials are invalid."""
    HTTPException(
        detail="Invalid credentials.",
        status_code=status.HTTP_401_UNAUTHORIZED
        )

class UserAlreadyExistsError(AppException):
    """Raised when a user already exists."""
    HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="Another User already exists."
        )

class MissingCredentialsError(AppException):
    """Raised when required authentication credentials are missing."""
    HTTPException(
        detail="Missing credentials. Enter either email or phone.",
        status_code=status.HTTP_400_BAD_REQUEST
        )