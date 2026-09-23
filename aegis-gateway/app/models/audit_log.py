from datetime import datetime
from uuid import UUID,uuid4
from sqlalchemy import Boolean,Integer,String,DateTime,ForeignKey,Float,Uuid
from sqlalchemy.orm import mapped_column,Mapped

from app.db import Base,utc_now

class AuditLog(Base):
  __tablename__="audit_logs"

  id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)

  request_id:Mapped[UUID]=mapped_column(Uuid,default=uuid4,unique=True)
  threat_score:Mapped[float]=mapped_column(Float,nullable=False)
  is_blocked:Mapped[bool]=mapped_column(Boolean,default=False,index=True)
  reason:Mapped[str|None]=mapped_column(String(100),nullable=True)
  llm_url:Mapped[str|None]=mapped_column(String(500),nullable=True)
  llm_name:Mapped[str|None]=mapped_column(String(100),nullable=True)
  latency_ms:Mapped[float]=mapped_column(Float)
  created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utc_now,index=True)

  user_id:Mapped[int]=mapped_column(
      Integer,
      ForeignKey("users.id",ondelete='CASCADE'),
      index=True,
      nullable=False
      )
  key_id:Mapped[int|None]=mapped_column(
      Integer,
      ForeignKey("api_keys.id",ondelete='SET NULL'),
      index=True,
      nullable=True,
      default=None
      )