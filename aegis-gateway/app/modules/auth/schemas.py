from pydantic import BaseModel,EmailStr,Field
from enum import Enum

from app.modules.token.schemas import TokenSchema
from app.modules.user.schemas import UserSchema,ProfileSchema
  
class RegisterSchema(UserSchema):
  """request schema used in registration process."""
  password:str=Field(...,
                    min_length=8,
                    max_length=128,
                    description="Password for future login.",
                    examples=["password@123"]
                    )

class LoginSchema(BaseModel):
  """request schema used in login process."""
  identifier:str=Field(...,
                      min_length=1,
                      max_length=255,
                      description="Email or Phone",
                      examples=["abc@example.com","9876543210"]
                      )
  password:str=Field(...,
                      min_length=8,
                      max_length=128,
                      description="Password for future login.",
                      examples=["password@123"]
                      )

class OAuthProvider(str, Enum):
    """constants for oauth"""
    GOOGLE = "google"
    GITHUB = "github"

class OauthLogin(BaseModel):
  """request schema for oauth login."""
  provider:OAuthProvider
  code:str

class OauthProfile(BaseModel):
  """request schema used in oauth login process."""
  email:EmailStr
  name:str|None=None
  oauth_provider:OAuthProvider = Field(..., max_length=50, examples=["google", "github"])
  oauth_id: str = Field(..., max_length=255, examples=["1082910391039102"])

class ResetSchema(BaseModel):
  """request schema for password reset"""
  new_password:str=Field(...,max_length=128,min_length=8)
  token:str

class ForgotSchema(BaseModel):
  """request schema for password reset"""
  email:EmailStr

class AuthResponse(BaseModel):
  """response schema for successful authentication."""
  user:ProfileSchema
  tokens:TokenSchema