from app.core.security import create_jwt_token,decode_jwt_token
from pydantic import BaseModel,ConfigDict

class TokenSchema(BaseModel):
  """response schema for tokens"""
  access_token:str
  refresh_token:str
  token_type:str="bearer"

class TokenPayloadSchema(BaseModel):
  """schema for token structure."""
  model_config=ConfigDict(from_attributes=True)
  
  id:int
  type:str
  exp:int


class TokenService:
  """provides services related to tokens"""

  @staticmethod
  def create_tokens(user_id:int):
    access_token=create_jwt_token(id=user_id,token_type="access")
    refresh_token=create_jwt_token(id=user_id,token_type="refresh")
    return access_token,refresh_token

  @staticmethod
  def decode_token(token:str)->TokenPayloadSchema|None:
    data=decode_jwt_token(token)
    if data is None:
      return data
    return TokenPayloadSchema.model_validate(data)