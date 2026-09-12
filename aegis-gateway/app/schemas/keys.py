from datetime import datetime
from pydantic import BaseModel,Field

class GenerateSchema(BaseModel):
  """request schema for generating key."""
  name:str|None=Field(default=None,max_length=100,examples=["Production Chatbot"])

class KeySchema(BaseModel):
  """response schema for key display."""
  id:int
  name:str|None=None
  prefix:str
  is_active:bool
  last_used:datetime|None=None
  created_at:datetime

class OneTimeSchema(BaseModel):
  """response schema to showcase key for only once after
    being generated so that user can copy it."""
  raw_key:str

class GenerateResponse(BaseModel):
  """response to be sent at key generation."""
  key:KeySchema
  secret:OneTimeSchema