from uuid import UUID
from pydantic import Field,BaseModel,ConfigDict

class Message(BaseModel):
    """base scehma for messages"""
    role:str
    content:str=Field(...,min_length=1)

class InspectRequest(BaseModel):
    """request schema for prompt inspection."""
    prompt:str=Field(...,min_length=1,description="Raw input text for LLM.")
    
class InspectResponse(BaseModel):
    """response schema for prompt inspection."""
    model_config=ConfigDict(from_attributes=True)
    
    request_id:UUID
    is_blocked:bool
    threat_score:float
    reason:str
    latency_ms:float

class ChatCompletionRequest(BaseModel):
    """request schema for inspect and upstream"""
    model:str
    messages:list[Message]=Field(...,min_length=1)

class ChatCompletionResponse(InspectResponse):
    """response schema for inpect and upstream"""
    response:dict|None=None