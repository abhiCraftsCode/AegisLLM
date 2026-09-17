from datetime import datetime
from uuid import UUID
from pydantic import BaseModel,ConfigDict

class LogSchema(BaseModel):
    """response schema for audit logs."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    request_id:UUID
    key_id: int | None = None
    threat_score: float
    is_blocked: bool
    reason: str | None = None
    latency_ms: float
    created_at: datetime

# class InspectRequest(BaseModel):
#     """request schema for prompt inspection."""
#     prompt:str=Field(...,min_length=1,description="Raw input text for LLM.")

# class InspectResponse(BaseModel):
#     """response schema for prompt inspection."""
#     request_id:UUID
#     is_blocked:bool
#     threat_score:float
#     reason:str
#     latency_ms:float

"""
class ChatCompletionRequest(BaseModel):
    model: str = Field(default="gpt-3.5-turbo")
    messages: List[Dict[str, Any]]
    temperature: Optional[float] = 0.7
    upstream_url: Optional[str] = Field(default="https://api.openai.com/v1/chat/completions")
"""