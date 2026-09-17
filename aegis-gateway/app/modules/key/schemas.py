from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict

class GenerateSchema(BaseModel):
  """request schema for generating key."""
  name:str|None=Field(default=None,max_length=100,examples=["Production Chatbot"])

class KeySchema(BaseModel):
  """response schema for key display."""
  model_config=ConfigDict(from_attributes=True)
  
  id:int
  name:str|None=None
  prefix:str
  is_active:bool
  last_used_at:datetime|None=None
  created_at:datetime

class GenerateResponse(BaseModel):
  """response to be sent at key generation."""
  key:KeySchema
  # only sent once in this generation response
  secret:str # raw key