from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.schemas import (
  RegisterSchema,
  AuthResponse,
  LoginSchema,
  TokenSchema,
  ProfileSchema
  )
from app.core.exceptions import (
  MissingCredentialsError,
  UserAlreadyExistsError,
  InvalidCredentialsError
  )
from app.models import User
from app.core.security import hash_password,verify_password
from app.modules.auth.repository import UserRepository
from app.modules.auth.tokenService import TokenService

class AuthService:
  """provides all services related to authentication"""

  @staticmethod
  async def register_user(data:RegisterSchema,db:AsyncSession)->AuthResponse:
    """register a new user."""
    #check if credentials are available
    if data.email is None and data.phone is None:
      raise MissingCredentialsError()

    # check if user already exist with those credentials
    repo=UserRepository(db)
    if data.email:
      existing_user=await repo.get_by_email(data.email)
      if existing_user is not None:
        raise UserAlreadyExistsError()
    if data.phone:
          existing_user=await repo.get_by_phone(data.phone)
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
      new_user=await repo.create_user(new_user)
      await db.commit()
    except Exception:
      await db.rollback()
      raise

    # issue tokens for session management
    access_token,refresh_token=TokenService.create_tokens(new_user.id)

    return AuthResponse(
      user=ProfileSchema.model_validate(new_user),
      tokens=TokenSchema(access_token=access_token,refresh_token=refresh_token)
    )

  @staticmethod
  async def login_user(data:LoginSchema,db:AsyncSession)->AuthResponse:
    """login a existing user."""

    #check for user availability
    repo=UserRepository(db)
    identifier=data.identifier.strip()
    user=await repo.get_by_identifier(identifier)
    # invalid identifier / oauth user but trying login by password / invalid password
    if user is None or user.password_hash is None or not verify_password(data.password,user.password_hash):
      raise InvalidCredentialsError()

    # issue tokens for session management
    access_token,refresh_token=TokenService.create_tokens(user.id)
    return AuthResponse(
      user=ProfileSchema.model_validate(user),
      tokens=TokenSchema(access_token=access_token,refresh_token=refresh_token)
    )

