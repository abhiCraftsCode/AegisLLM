from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.modules.user.repository import UserRepository
from app.modules.user.schemas import (
  ProfileSchema,
  UpdateSchema,
  PasswordSchema
)
from app.models import User
from app.core.security import verify_password,hash_password
from app.core.exceptions import (
  UserNotFoundError,
  UserAlreadyExistsError,
  InvalidCredentialsError
)

class UserService:
  """provide all services related to user data."""

  @staticmethod
  async def create_user(user:User,db:AsyncSession)->ProfileSchema:
    """create a new user row."""
    repo=UserRepository(db)
    try:
      user=await repo.create(user)
      await db.commit()
    except Exception:
      await db.rollback()
      raise

    return ProfileSchema.model_validate(user)

  @staticmethod
  async def get_user(identifier:str,db:AsyncSession)->ProfileSchema|None:
    """get a user row"""
    # returning without password
    #for identifier basis fetch
    repo=UserRepository(db)
    user=await repo.get_by_identifier(identifier)
    if user is None:
      return None
    return ProfileSchema.model_validate(user)

  @staticmethod
  async def find_user(identifier:str,db:AsyncSession)->User|None:
    """find a user row else none"""
    repo=UserRepository(db)
    # allowed returning none because some function may require user not to be available
    # returning model instead of schema to match password
    return await repo.get_by_identifier(identifier)

  @staticmethod
  async def update(data:UpdateSchema,id:int,db:AsyncSession)->ProfileSchema:
    """update fileds of user row."""
    repo=UserRepository(db)
    user=await repo.get_by_id(id)
    if user is None:
      raise UserNotFoundError()
    try:
      if data.email is not None:
        user.email=data.email
      if data.phone is not None:
        user.phone=data.phone
      if data.name is not None:
        user.name=data.name
      await db.commit()
      await db.refresh(user)
    except IntegrityError:
      await db.rollback()
      raise UserAlreadyExistsError()
    except Exception:
      await db.rollback()
      raise

    return ProfileSchema.model_validate(user)

  @staticmethod
  async def password_update(data:PasswordSchema,id:int,db:AsyncSession)->None:
    """verifies and updates password"""
    curr,new=data.curr_password,data.new_password
    repo=UserRepository(db)
    user=await repo.get_by_id(id)
    if user is None:
      raise UserNotFoundError()
    if user.password_hash is not None and not verify_password(curr,user.password_hash):
      raise InvalidCredentialsError()
    try:
      user.password_hash=hash_password(new)
      await db.commit()
    except Exception:
      await db.rollback()
      raise
  
  @staticmethod
  async def get_profile(id:int,db:AsyncSession)->ProfileSchema:
    """fetch the profile of a user"""
    repo=UserRepository(db)
    user=await repo.get_by_id(id)
    if user is None:
      raise UserNotFoundError()
    return ProfileSchema.model_validate(user)