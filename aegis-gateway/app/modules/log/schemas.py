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
    llm_name:str|None=None
    llm_url:str|None=None

class PageResponse(BaseModel):
  """resonse schema for audit-logs page-wise to display."""
  items:list[LogSchema]
  page:int
  size:int
  total:int
  pages:int