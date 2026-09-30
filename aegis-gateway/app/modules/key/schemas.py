from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict,field_validator

class GenerateSchema(BaseModel):
  """request schema for generating key."""
  name:str|None=Field(default=None,max_length=100,examples=["Production Chatbot"])
  llm_name:str|None=Field(default=None,max_length=100,examples=["My LLM"])
  llm_auth:str|None=Field(default=None,examples=["xx-api-key-xx"])
  llm_url:str|None=Field(
    default=None,
    max_length=500,
    examples=["//https:/example.com/v1/chat/completions"]
    )
  @field_validator("llm_auth")
  @classmethod
  def sanitize_llm_auth(cls, v: str | None) -> str | None:
      if not v:
          return None
      v = v.strip()
      # Automatically strip "Bearer " or "bearer " if user pasted it
      if v.lower().startswith("bearer "):
          return v[7:].strip()
      return v

class KeySchema(BaseModel):
  """response schema for key."""
  model_config=ConfigDict(from_attributes=True)
  
  id:int
  user_id:int
  name:str|None=None
  prefix:str
  is_active:bool
  last_used_at:datetime|None=None
  created_at:datetime
  llm_name:str|None
  llm_url:str|None
  
class GenerateResponse(BaseModel):
  """response to be sent at key generation."""
  key:KeySchema
  # only sent once in this generation response
  secret:str # raw key

class UpdateSchema(BaseModel):
  """request schema to update fields of api-key"""
  name:str|None=Field(default=None,max_length=100,examples=["Production Chatbot"])
  llm_name:str|None=Field(default=None,max_length=100,examples=["My LLM"])
  llm_auth:str|None=Field(default=None,examples=["xx-api-key-xx"])
  llm_url:str|None=Field(
    default=None,
    max_length=500,
    examples=["//https:/example.com/v1/chat/completions"]
    )
  @field_validator("llm_auth")
  @classmethod
  def sanitize_llm_auth(cls, v: str | None) -> str | None:
      if not v:
          return None
      v = v.strip()
      # Automatically strip "Bearer " or "bearer " if user pasted it
      if v.lower().startswith("bearer "):
          return v[7:].strip()
      return v

class ConfigInternalResponse(BaseModel):
  """response schema for updated credentials"""
  llm_url:str
  llm_auth:str

class PageResponse(BaseModel):
  """resonse schema for keys page-wise to display."""
  items:list[KeySchema]
  page:int #current page
  size:int #page size
  total:int #total keys
  pages:int #total pages