from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.schemas import (
  RegisterSchema,
  AuthResponse,
  LoginSchema,
  ForgotSchema,
  ResetSchema,
  OauthLogin
  )
from app.core.oauth import get_oauth_user
from app.modules.user.schemas import ProfileSchema,UpdateSchema
from app.core.exceptions import (
  MissingCredentialsError,
  UserAlreadyExistsError,
  UnauthorizedUserError,
  InvalidCredentialsError,
  InvalidExpiredTokenError
  )
from app.models import User
from app.core.mail import send_mail
from app.core.security import hash_password,verify_password
from app.modules.user.service import UserService
from app.modules.token.service import TokenService

class AuthService:
  """provides all services related to authentication"""

  @staticmethod
  async def forgot_request(data:ForgotSchema,bgt:BackgroundTasks,db:AsyncSession)->None:
    """generate and trigger a password reset link"""
    #only email based recovery now 
    user=await UserService.get_user(data.email,db)
    if not user or not user.is_active:
      return #safety measure to fool attack and hide credential mismatch info
    #dispatch email using email 
    token=TokenService.reset_token(data.email)
    bgt.add_task(send_mail,data.email,token)

  @staticmethod
  async def reset_request(data:ResetSchema,db:AsyncSession)->None:
    """verify and reset password"""
    payload=TokenService.decode_token(data.token)
    if payload !="refresh" or not isinstance(payload.data,str):
      raise InvalidExpiredTokenError()
    email=payload.data
    if not email:
      raise MissingCredentialsError()
    user=await UserService.find_user(email,db)
    if not user or not user.is_active:
      raise UnauthorizedUserError()
    if user.updated_at is not None:
      time=int(user.updated_at.timestamp())
      if time>payload.iat:
        raise InvalidExpiredTokenError()
    try:
      user.password_hash=hash_password(data.new_password)
      await db.commit()
    except Exception:
      await db.rollback()
      raise

  @staticmethod
  async def oauth(payload:OauthLogin,db:AsyncSession)->AuthResponse:
    profile=await get_oauth_user(payload.provider,payload.code)
    user=await UserService.get_user(profile.email,db)
    if user:
      #existing user 
      if user.oauth_provider is None:
        # first time oauth of existing
        user=await UserService.update(
            data=UpdateSchema(
            oauth_provider=profile.oauth_provider,
            oauth_id=profile.oauth_id
          ),
          id=user.id,
          db=db)
    else:
      new_user=User(
        email=profile.email,
        name=profile.name,
        password_hash=None,
        phone=None,
        oauth_provider=profile.oauth_provider,
        oauth_id=profile.oauth_id
      )
      user=await UserService.create_user(new_user,db)
    return AuthResponse(
      user=user,
      tokens=TokenService.create_tokens(user.id)
    )

  
    
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

    new_user=await UserService.create_user(new_user,db)

    # issue tokens for session management
    tokens=TokenService.create_tokens(new_user.id)

    return AuthResponse(
      user=new_user,
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
    if (
      user is None 
      or user.password_hash is None 
      or not verify_password(data.password,user.password_hash)
    ):
      raise InvalidCredentialsError()

    # issue tokens for session management
    tokens=TokenService.create_tokens(user.id)
    return AuthResponse(
      user=ProfileSchema.model_validate(user),
      tokens=tokens
    )

