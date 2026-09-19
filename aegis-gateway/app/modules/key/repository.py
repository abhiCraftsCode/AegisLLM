from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func

from app.models import ApiKey

class KeyRepository:
  """repository for api_keys table"""
  def __init__(self,db:AsyncSession) -> None:
    self.db=db

  async def get_by_id(self,id:int)->ApiKey|None:
    """fetch row with matching row id"""
    stmt=select(ApiKey).where(ApiKey.id==id)
    return (await self.db.execute(stmt)).scalar_one_or_none()

  async def get_by_hash(self,hash:str)->ApiKey|None:
    """fetch row with matching encrypted hash"""
    stmt=select(ApiKey).where(ApiKey.key_hash==hash)
    return (await self.db.execute(stmt)).scalar_one_or_none()

  async def get_all_for_user(self,user_id:int,page:int,size:int)->tuple[list[ApiKey],int]:
    """fetch all key rows that belong to the user with this user_id"""
    """pagination applied"""
    offset=(page-1)*size
    stmt=(
      select(ApiKey)
      .where(ApiKey.user_id==user_id)
      .order_by(ApiKey.created_at.desc())
      .offset(offset)
      .limit(size)
    )
    ctstmt=select(func.count(ApiKey.id)).where(ApiKey.user_id==user_id)
    keys=list((await self.db.execute(stmt)).scalars().all())
    total=(await self.db.execute(ctstmt)).scalar_one()
    return (keys,total)

  async def create(self,key:ApiKey)->ApiKey:
    """creae a new row in api_keys table."""
    self.db.add(key)
    await self.db.flush()
    await self.db.refresh(key)
    return key

  async def deactivate(self,key:ApiKey)->None:
    """revokes the active status of the key and marks it inactive permanently"""
    key.is_active=False
