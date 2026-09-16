from app.core.security import create_jwt_token,decode_jwt_token
from app.modules.token.schemas import TokenPayloadSchema

class TokenService:
  """provides services related to tokens"""

  @staticmethod
  def create_tokens(user_id:int):
    """create both access and refresh tokens"""
    access_token=create_jwt_token(id=user_id,token_type="access")
    refresh_token=create_jwt_token(id=user_id,token_type="refresh")
    return access_token,refresh_token

  @staticmethod
  def decode_token(token:str)->TokenPayloadSchema|None:
    """decodes the token into respective values or no value"""
    data=decode_jwt_token(token)
    if data is None:
      return data
    return TokenPayloadSchema.model_validate(data)