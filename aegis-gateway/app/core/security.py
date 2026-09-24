import base64
import hashlib
from cryptography.fernet import Fernet
from datetime import timedelta
from typing import Any
from jose import jwt,JWTError
from pwdlib import PasswordHash

from app.core.config import settings
from app.db import utc_now

pwd=PasswordHash.recommended()

def _get_fernet_key() -> bytes:
  """Derive a valid 32-byte url-safe base64 key from your SECRET_KEY"""
  key_digest = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
  return base64.urlsafe_b64encode(key_digest)

def encrypt_field(plain_text: str | None) -> str | None:
  """string encryption-retrievalble"""
  if not plain_text:
      return None
  f = Fernet(_get_fernet_key())
  return f.encrypt(plain_text.encode("utf-8")).decode("utf-8")

def decrypt_field(cipher_text: str | None) -> str | None:
  """string decryption"""
  if not cipher_text:
      return None
  f = Fernet(_get_fernet_key())
  return f.decrypt(cipher_text.encode("utf-8")).decode("utf-8")

def verify_password(plain_password:str,hashed_password:str)->bool:
  """verigy raw password against stored hash password."""
  return pwd.verify(plain_password,hashed_password)

def hash_password(password:str)->str:
  """generate hashed password for raw passwrod."""
  return pwd.hash(password)

def hash_str(raw_str: str) -> str:
  """Generate SHA-256 digest of string (api keys, prompts)."""
  """non retrievalbe"""
  return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

def create_jwt_token(data:int|str,token_type:str='access') -> str:
    """Issue JWT Tokens."""
    now,expire=utc_now(),''
    if token_type == "refresh":
      expire=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    elif token_type=="reset":
      expire=now+timedelta(minutes=settings.RESET_TOKEN_EXPIRE_MINUTES)
    else:
      expire =now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"iat":now,"exp": expire, "data":data, "token_type": token_type}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_jwt_token(token: str) -> dict[str, Any]|None:
    """Decode and validate a JWT string against secret key."""
    try:
      payload=jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
      return payload
    except (JWTError,ValueError):
      #invalid token must be checked in parent caller
      return None