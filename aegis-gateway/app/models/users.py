from datetime import datetime,timezone
from sqlalchemy import Boolean
from sqlalchemy.orm import mapped_column,relationship,Mapped
from app.db.base import Base

class User(Base):
  pass