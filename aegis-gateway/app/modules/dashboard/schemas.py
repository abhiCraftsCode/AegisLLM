from datetime import date
from pydantic import BaseModel

class DaySchema(BaseModel):
  """response schema for single day activity"""
  date:date
  total_requests:int
  blocked_requests:int

class WeekSchema(BaseModel):
  """response schema for per week activity"""
  week:int
  start_date:date
  end_date:date
  days:list[DaySchema]

class StatSchema(BaseModel):
  """response schema for dashboard statistics"""
  total_requests:int
  allowed_requests:int
  blocked_requests:int
  block_rate:float

  avg_latency_ms:float

  avg_threat_score:float
  highest_threat_score:float

  total_keys:int
  active_keys:int

  activity:list[WeekSchema]