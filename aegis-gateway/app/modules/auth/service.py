from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.schemas import (
  RegisterSchema,
  AuthResponse,
  LoginSchema
  )
from app.modules.user.schemas import ProfileSchema
from app.core.exceptions import (
  MissingCredentialsError,
  UserAlreadyExistsError,
  InvalidCredentialsError
  )
from app.models import User
from app.core.security import hash_password,verify_password
from app.modules.user.service import UserService
from app.modules.token.service import TokenService

class AuthService:
  """provides all services related to authentication"""

  @staticmethod
  async def register_user(data:RegisterSchema,db:AsyncSession)->AuthResponse:
    """register a new user."""
    #check if credentials are available
    if data.email is None and data.phone is None:
      raise MissingCredentialsError()

    # check if user already exist with those credentials
    if data.email:
      existing_user=await UserService.find_user(data.email,db)
      if existing_user is not None:
        raise UserAlreadyExistsError()
    if data.phone:
      existing_user=await UserService.find_user(data.phone,db)
      if existing_user is not None:
        raise UserAlreadyExistsError()

    # creating new user
    new_user=User(
      name=data.name,
      email=data.email,
      phone=data.phone,
      password_hash=hash_password(data.password)
    )
    # inserting and commiting to database
    try:
      new_user=await UserService.create_user(new_user,db)
      await db.commit()
    except Exception:
      await db.rollback()
      raise

    # issue tokens for session management
    tokens=TokenService.create_tokens(new_user.id)

    return AuthResponse(
      user=ProfileSchema.model_validate(new_user),
      tokens=tokens
    )

  @staticmethod
  async def login_user(data:LoginSchema,db:AsyncSession)->AuthResponse:
    """login a existing user."""

    identifier=data.identifier.strip()
    if len(identifier)==0:
      raise MissingCredentialsError()
    
    #check for user availability
    user=await UserService.find_user(identifier,db)

    # invalid identifier / oauth user but trying login by password / invalid password
    # why not user not found and invalid is because while login it is invalid user.
    if user is None or user.password_hash is None or not verify_password(data.password,user.password_hash):
      raise InvalidCredentialsError()

    # issue tokens for session management
    tokens=TokenService.create_tokens(user.id)
    return AuthResponse(
      user=ProfileSchema.model_validate(user),
      tokens=tokens
    )

