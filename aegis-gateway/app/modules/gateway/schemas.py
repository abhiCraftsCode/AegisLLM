from uuid import UUID
from pydantic import Field,BaseModel

class InspectRequest(BaseModel):
    """request schema for prompt inspection."""
    prompt:str=Field(...,min_length=1,description="Raw input text for LLM.")

class InspectResponse(BaseModel):
    """response schema for prompt inspection."""
    request_id:UUID
    is_blocked:bool
    threat_score:float
    reason:str
    latency_ms:float

class ChatCompletionRequest(InspectRequest):
    """request schema for inspect and upstream"""
    llm_url:str=Field(...,min_length=1,description="Url of LLM.")
    llm_api_key:str=Field(...,min_length=1,description="Raw input text for LLM.")

class ChatCompletionResponse(InspectResponse):
    """response schema for inpect and upstream"""
    response:dict|None=None