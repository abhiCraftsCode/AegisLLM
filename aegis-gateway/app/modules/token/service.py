from app.core.security import create_jwt_token,decode_jwt_token
from app.modules.token.schemas import TokenPayloadSchema,TokenSchema
from app.core.exceptions import InvalidExpiredTokenError

class TokenService:
  """provides services related to tokens"""

  @staticmethod
  def create_tokens(user_id:int)->TokenSchema:
    """create both access and refresh tokens"""
    access_token=create_jwt_token(user_id,token_type="access")
    refresh_token=create_jwt_token(user_id,token_type="refresh")
    tokens=TokenSchema(access_token=access_token,refresh_token=refresh_token)
    return tokens

  @staticmethod
  def decode_token(token:str)->TokenPayloadSchema:
    """decodes the token into respective values or no value"""
    payload=decode_jwt_token(token)
    if payload is None:
      raise InvalidExpiredTokenError()
    return TokenPayloadSchema.model_validate(payload)

  @staticmethod
  def reset_token(email:str)->str:
    """generate a very short lived token."""
    token=create_jwt_token(email,token_type="reset")
    return token
