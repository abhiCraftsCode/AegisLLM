from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict,computed_field

class GenerateSchema(BaseModel):
  """request schema for generating key."""
  name:str|None=Field(default=None,max_length=100,examples=["Production Chatbot"])
  llm_name:str|None=Field(default=None,max_length=100,examples=["My LLM"])
  llm_auth:str|None=Field(default=None,examples=["Bearer xx-api-key-xx"])
  llm_url:str|None=Field(
    default=None,
    max_length=500,
    examples=["//https:/example.com/v1/chat/completions"]
    )

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
  @computed_field
  @property
  def has_llm_auth(self) -> bool:
    return (
      getattr(self, "llm_auth", None) is not None 
      and getattr(self,"llm_url",None) is not None
    )

class GenerateResponse(BaseModel):
  """response to be sent at key generation."""
  key:KeySchema
  # only sent once in this generation response
  secret:str # raw key

class UpstreamConfig(BaseModel):
  """request to be sent for upstream forwarding"""
  llm_name:str|None=Field(default=None,max_length=100)
  llm_url:str|None=Field(default=None,max_length=500)
  llm_auth:str|None=None

class ConfigResponse(BaseModel):
  """response schema for updated credentials"""
  llm_url:str
  llm_auth:str

class PageResponse(BaseModel):
  """resonse schema for keys page-wise to display."""
  items:list[KeySchema]
  page:int
  size:int
  total:int
  pages:int