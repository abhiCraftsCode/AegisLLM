from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

from app.core.security import hash_str
from app.modules.token.service import TokenService
from app.modules.user.service import UserService
from app.modules.key.service import KeyService
from app.modules.user.schemas import ProfileSchema
from app.modules.key.schemas import KeySchema
from app.db import LocalSession
from app.core.engine import SecurityEngine
from app.core.exceptions import (
    MissingTokenError,
    AccessTokenError,
    InactiveKeyError,
    MissingKeyError
    )

bearer_scheme = HTTPBearer()

#dependency helper function to connect to db
async def get_db()->AsyncGenerator[AsyncSession,None]:
  """dependency for db connection."""
  async with LocalSession() as session:
    try:
      yield session
    finally:
      await session.close()

#dependency function to get search engine
def get_engine()->SecurityEngine:
    raise NotImplementedError

# dependency function to mimic isAuth for jwt
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> ProfileSchema:
    """dependency for is_auth, fetches the profile of logged in user."""
    """authenticate the logged in user"""
    token = credentials.credentials

    # chechk if token decodesuccessfully
    if token is None or len(token)==0:
        raise MissingTokenError()

    payload = TokenService.decode_token(token)

    # check if token is access token
    if payload.type != "access":
        raise AccessTokenError()

    user_id = payload.id
    user = await UserService.get_profile(user_id,db)

    return user

#dependency function to mimic is_auth for api key
async def get_current_api_key(
    credentials:HTTPAuthorizationCredentials=Depends(bearer_scheme),
    db:AsyncSession=Depends(get_db)
)->KeySchema:
    """authenticate an aegis API key"""

    raw_key=credentials.credentials

    if raw_key is None or len(raw_key)==0:
        raise MissingKeyError()
    
    hash_key=hash_str(raw_key)

    key=await KeyService.get_hash_key(hash_key,db)

    if not key.is_active:
        raise InactiveKeyError()

    return key