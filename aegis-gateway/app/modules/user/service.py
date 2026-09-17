from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.repository import UserRepository
from app.modules.user.schemas import ProfileSchema
from app.models.user import User
from app.core.exceptions import UserNotFoundError

class UserService:
  """provide all services related to user data."""

  @staticmethod
  async def create_user(user:User,db:AsyncSession):
    """create a new user row."""
    repo=UserRepository(db)
    user=await repo.create(user)
    return user

  @staticmethod
  async def find_user(identifier,db)->User|None:
    """find a user row else none"""
    repo=UserRepository(db)
    # allowed returning none because some function may require user not to be available
    return await repo.get_by_identifier(identifier)
    
  @staticmethod
  async def get_profile(id:int,db:AsyncSession)->ProfileSchema:
    """fetch the profile of a user"""
    repo=UserRepository(db)
    user=await repo.get_by_id(id)
    if user is None:
      raise UserNotFoundError()
    return ProfileSchema.model_validate(user)