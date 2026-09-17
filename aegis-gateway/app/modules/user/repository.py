from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_,select

from app.models.user import User

class UserRepository:
  """repository for users table"""
  def __init__(self, db: AsyncSession):
        self.db = db

  async def get_by_identifier(self,identifier:str)->User|None:
    """fetch record matching either email or phone"""
    stmt=select(User).where(or_(User.email==identifier,User.phone==identifier))
    return (await self.db.execute(stmt)).scalar_one_or_none()

  async def get_by_email(self,email:str)->User|None:
      """fetch record matching the email"""
      stmt=select(User).where(User.email==email)
      return (await self.db.execute(stmt)).scalar_one_or_none()

  async def get_by_phone(self,phone:str)->User|None:
      """fetch record matching the phone"""
      stmt=select(User).where(User.phone==phone)
      return (await self.db.execute(stmt)).scalar_one_or_none()

  async def get_by_id(self,user_id:int)->User|None:
        """fetch record matching the row id"""
        stmt=select(User).where(User.id==user_id)
        return (await self.db.execute(stmt)).scalar_one_or_none()

  async def create(self,user:User)->User:
      """add new user row"""
      self.db.add(user)
      await self.db.flush()
      await self.db.refresh(user)
      return user

  