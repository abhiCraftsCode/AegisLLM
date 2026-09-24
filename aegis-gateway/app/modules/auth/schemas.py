from pydantic import BaseModel,EmailStr,Field

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