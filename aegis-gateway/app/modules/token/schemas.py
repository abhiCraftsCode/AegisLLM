from pydantic import BaseModel,ConfigDict

class TokenSchema(BaseModel):
  """response schema for tokens"""
  access_token:str
  refresh_token:str
  token_type:str="bearer"

class TokenPayloadSchema(BaseModel):
  """schema for token structure."""
  model_config=ConfigDict(from_attributes=True)
  
  id:int
  type:str
  exp:int

