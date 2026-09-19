import secrets
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_str
from app.core.exceptions import (
  UnauthorizedUserError,
  KeyNotFoundError,
  LLMCredentialsError
)
from app.modules.key.repository import KeyRepository
from app.models import ApiKey
from app.modules.key.schemas import (
  KeySchema,
  GenerateResponse,
  GenerateSchema,
  UpstreamConfig,
  ConfigResponse
)

class KeyService:
  """services related to api keys of the app"""

  @staticmethod
  async def generate_key(data:GenerateSchema,user_id:int,db:AsyncSession)->GenerateResponse:
    """generate a new key for user"""
    repo=KeyRepository(db)

    #generate a new secret key
    raw_key=f"aegis_{secrets.token_urlsafe(32)}"
    
    new_key=ApiKey(
      prefix=f"{raw_key[:10]}...",
      name=data.name,
      key_hash=hash_str(raw_key), # encrypted key
      user_id=user_id,
      llm_name=data.llm_name,
      llm_url=data.llm_url,
      llm_auth=data.llm_auth
    )
    try:
      new_key=await repo.create(new_key)
      await db.commit()
    except Exception:
      await db.rollback()
      raise

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
      raise UnauthorizedUserError()

    try:
      await repo.deactivate(key)  
      await db.commit()
    except Exception:
      await db.rollback()
      raise
    #return none because success deletion code will be returned 

  @staticmethod
  async def get_all_keys(user_id:int,db:AsyncSession)->list[KeySchema]:
    """fetch all the keys of user"""
    repo=KeyRepository(db)
    keys=await repo.get_all_for_user(user_id)
    return [KeySchema.model_validate(key) for key in keys]

  @staticmethod
  async def get_key(key_id:int,user_id:int,db:AsyncSession)->KeySchema:
    """fetch a particular key of user"""
    repo=KeyRepository(db)
    key=await repo.get_by_id(key_id)

    if key is None:
      raise KeyNotFoundError()

    if key.user_id != user_id:
      raise UnauthorizedUserError()

    return KeySchema.model_validate(key)

  @staticmethod
  async def get_hash_key(hash:str,db:AsyncSession)->KeySchema:
    """fetch key with particular hash value"""
    repo=KeyRepository(db)
    key=await repo.get_by_hash(hash)
    
    if key is None:
      raise KeyNotFoundError()
    
    return KeySchema.model_validate(key)

  @staticmethod
  async def update(
    key_id:int,
    user_id:int,
    data:UpstreamConfig,
    db:AsyncSession
    )->KeySchema:
    """update the fields of row"""
    repo=KeyRepository(db)
    key=await repo.get_by_id(key_id)

    if key is None:
      raise KeyNotFoundError()

    if key.user_id!=user_id:
      raise UnauthorizedUserError()

    try:
      key.llm_auth=data.llm_auth
      key.llm_url=data.llm_url
      key.llm_name=data.llm_name
      await db.commit()
      await db.refresh(key)
    except Exception:
      await db.rollback()
      raise

    return KeySchema.model_validate(key)

  @staticmethod
  async def get_llm_config(key_id,db:AsyncSession)->ConfigResponse:
    """fetches llm  configuration of a key"""
    repo=KeyRepository(db)
    key=await repo.get_by_id(key_id)
    if key is None or key.llm_url is None or key.llm_auth is None:
      raise LLMCredentialsError()

    return ConfigResponse(
      llm_auth=key.llm_auth,
      llm_url=key.llm_url
    )

  