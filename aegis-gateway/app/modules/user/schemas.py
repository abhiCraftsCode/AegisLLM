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
  
class ProfileSchema(UserSchema):
  """response schema for user."""
  model_config=ConfigDict(from_attributes=True)

  id:int
  oauth_provider:str|None=None
  is_active:bool
  created_at:datetime

class UpdateSchema(BaseModel):
  """request schema for profile updation."""
  name:str|None=Field(default=None,min_length=2,max_length=100)
  email:EmailStr|None=None
  phone:str|None=Field(default=None,max_length=15,min_length=10)
  password:str|None=Field(default=None,max_length=128,min_length=8)
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

class PasswordSchema(BaseModel):
  """request schema for password reset"""
  new_password:str=Field(...,max_length=128,min_length=8)
  curr_password:str|None=Field(default=None,max_length=128,min_length=8)