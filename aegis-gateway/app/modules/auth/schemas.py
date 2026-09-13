from datetime import datetime
from pydantic import BaseModel,EmailStr,Field,ConfigDict,field_validator

class UserSchema(BaseModel):
  """base schema for user."""
  name:str=Field(...,min_length=2,max_length=100,examples=["Shah Rukh Khan"])
  email:EmailStr|None=Field(default=None,examples=["abc@example.com"])
  phone:str|None=Field(default=None,max_length=15,min_length=10,examples=["+919876543210","9876543210"])
  @field_validator("phone",mode="before")
  @classmethod
  def validate_phone(cls, value):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("Phone number must be a string.")
    value = value.strip()
    if value.startswith("+91"):
        number = value[3:]
    else:
        number = value
    if len(number) != 10:
        raise ValueError("Indian phone number must contain 10 digits.")
    if not number.isdigit():
        raise ValueError("Phone number must contain only digits.")
    if number[0] not in "6789":
        raise ValueError(
            "Indian phone number must start with 6, 7, 8, or 9."
        )
    return f"+91{number}"
  
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
  identifier:str=Field(...,min_length=1,max_length=255,examples=["abc@example.com","9876543210"])
  password:str=Field(...,
                      min_length=8,
                      max_length=128,
                      description="Password for future login.",
                      examples=["password@123"]
                      )

class OauthSchema(BaseModel):
  """request schema used in oauth login process."""
  email:EmailStr
  name:str
  oauth_provider: str = Field(..., max_length=50, examples=["google", "github"])
  oauth_id: str = Field(..., max_length=255, examples=["1082910391039102"])

class ProfileSchema(UserSchema):
  """response schema for user."""
  model_config=ConfigDict(from_attributes=True)

  id:int
  oauth_provider:str|None=None
  is_active:bool
  created_at:datetime

class TokenSchema(BaseModel):
  """response schema for tokens"""
  access_token:str
  refresh_token:str
  token_type:str="bearer"

class TokenPayloadSchema(BaseModel):
  """schema for token structure."""
  id:int
  type:str
  exp:int

class AuthResponse(BaseModel):
  """response schema for successful authentication."""
  user:ProfileSchema
  tokens:TokenSchema