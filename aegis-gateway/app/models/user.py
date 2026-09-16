from datetime import datetime
from sqlalchemy import Boolean,Integer,String,DateTime
from sqlalchemy.orm import mapped_column,Mapped
from app.db.base import Base,utc_now

class User(Base):
  __tablename__="users"

  id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,index=True)

  name:Mapped[str]=mapped_column(String(100),nullable=False)
  email:Mapped[str|None]=mapped_column(String(255),unique=True,index=True,nullable=True)
  phone:Mapped[str|None]=mapped_column(String(15),unique=True,index=True,nullable=True)
  password_hash:Mapped[str|None]=mapped_column(String(255),nullable=True)
  oauth_provider:Mapped[str|None]=mapped_column(String(50),nullable=True)
  oauth_id:Mapped[str|None]=mapped_column(String(255),nullable=True,index=True)
  is_active:Mapped[bool]=mapped_column(Boolean,default=True)
  created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utc_now)
  updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utc_now,onupdate=utc_now)