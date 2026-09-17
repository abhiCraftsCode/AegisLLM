import secrets
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_str
from app.core.exceptions import UnauthorizedKeyError,KeyNotFoundError
from app.modules.key.repository import KeyRepository
from app.models.apiKey import ApiKey
from app.modules.key.schemas import (
  KeySchema,
  GenerateResponse,
  GenerateSchema
)

class KeyService:
  """services related to api keys of the app"""

  @staticmethod
  async def generate_key(data:GenerateSchema,user_id:int,db:AsyncSession)->GenerateResponse:
    """generate a new key for user"""
    repo=KeyRepository(db)

    #generate a new secret key
    raw_key=f"aegis_{secrets.token_urlsafe(32)}"
    #encrypt the key 
    hash_key=hash_str(raw_key)
    prefix=f"{raw_key[:10]}..."
    new_key=ApiKey(
      prefix=prefix,
      name=data.name,
      key_hash=hash_key,
      user_id=user_id
    )

    new_key=await repo.create(new_key)
    await db.commit()

    # structure the response for one time key showing
    key=GenerateResponse(
      key=KeySchema.model_validate(new_key),
      secret=raw_key
    )
    return key

  @staticmethod
  async def deactivate_key(key_id:int,user_id,db:AsyncSession)->None:
    """deactivate and old key of user only"""
    repo=KeyRepository(db)
    key=await repo.get_by_id(key_id)

    # security checks
    if key is None:
      raise KeyNotFoundError()

    if key.user_id != user_id:
      raise UnauthorizedKeyError()

    await repo.deactivate(key)  
    await db.commit()
    #return none because success deletion code will be returned 

  @staticmethod
  async def get_all_keys(user_id:int,db:AsyncSession)->list[KeySchema]:
    """fetch all the keys of user"""
    repo=KeyRepository(db)
    keys=await repo.get_all_for_user(user_id)
    return [KeySchema.model_validate(key) for key in keys]

  @staticmethod
  async def get_key(key_id,user_id:int,db:AsyncSession)->KeySchema:
    """fetch a particular key of user"""
    repo=KeyRepository(db)
    key=await repo.get_by_id(key_id)

    if key is None:
      raise KeyNotFoundError()

    if key.user_id != user_id:
      raise UnauthorizedKeyError()

    return KeySchema.model_validate(key)