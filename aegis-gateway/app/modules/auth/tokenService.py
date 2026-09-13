from app.core.security import create_jwt_token
  
class TokenService:
  """provides services related to tokens"""

  @staticmethod
  def create_tokens(user_id:int):
    access_token=create_jwt_token(id=user_id,token_type="access")
    refresh_token=create_jwt_token(id=user_id,token_type="refresh")
    return access_token,refresh_token
    