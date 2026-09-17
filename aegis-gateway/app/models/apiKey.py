from datetime import datetime
from sqlalchemy import Boolean,Integer,String,DateTime,ForeignKey
from sqlalchemy.orm import mapped_column,Mapped

from app.db.base import Base,utc_now

class ApiKey(Base):
  __tablename__="api_keys"

  id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,autoincrement=True)

  name:Mapped[str|None]=mapped_column(String(100),nullable=True)
  prefix:Mapped[str]=mapped_column(String(32),nullable=False)
  key_hash:Mapped[str]=mapped_column(String(64),nullable=False,unique=True,index=True)
  is_active:Mapped[bool]=mapped_column(Boolean,default=True)
  last_used_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
  created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utc_now)

  user_id:Mapped[int]=mapped_column(
    Integer,
    ForeignKey("users.id",ondelete='CASCADE'),
    index=True,
    nullable=False
    )