import hashlib
from datetime import datetime,timedelta,timezone
from typing import Any
from jose import jwt,JWTError
from pwdlib import PasswordHash

from app.core.config import settings
from app.db.base import utc_now

pwd=PasswordHash.recommended()

def verify_password(plain_password:str,hashed_password:str)->bool:
  """verigy raw password against stored hash password."""
  return pwd.verify(plain_password,hashed_password)

def hash_password(password:str)->str:
  """generate hashed password for raw passwrod."""
  return pwd.hash(password)

def hash_str(raw_str: str) -> str:
    """Generate SHA-256 digest of string (api keys, prompts)."""
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

def create_jwt_token(data:int|str,token_type:str='access') -> str:
    """Issue JWT Tokens."""
    expire=''
    if token_type == "refresh":
      expire=utc_now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    elif token_type=="reset":
      expire= utc_now()+timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)
    else:
      expire = utc_now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"exp": expire, "data":id, "type": token_type}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_jwt_token(token: str) -> dict[str, Any]|None:
    """Decode and validate a JWT string against secret key."""
    try:
      payload=jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
      return payload
    except JWTError:
      #invalid token must be checked in parent caller
      return None