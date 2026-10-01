from typing import Any
from uuid import UUID
from pydantic import BaseModel,ConfigDict

class InspectResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    
    request_id:UUID
    is_blocked:bool
    threat_score:float
    reason:str
    latency_ms:float

class ChatCompletionResponse(InspectResponse):
    response:dict[str,Any]|None=None