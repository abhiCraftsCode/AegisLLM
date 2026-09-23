from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuditLog

class LogRepository:
  """repository for audit_logs table."""
  def __init__(self,db:AsyncSession) -> None:
    self.db=db

  async def create(self,log:AuditLog)->AuditLog:
    """add a new log row"""
    self.db.add(log)
    await self.db.flush()
    await self.db.refresh(log)
    return log

  async def get_by_id(self,id:int)->AuditLog|None:
    """fetch row with matching id"""
    res=await self.db.execute(select(AuditLog).where(AuditLog.id==id))
    return res.scalar_one_or_none()

  async def get_all_for_user(self,user_id:int,page:int,size:int)->tuple[list[AuditLog],int]:
    """fetch all logs of user"""
    offset=(page-1)*size
    logs=(await self.db.execute(
      select(AuditLog)
      .where(AuditLog.user_id==user_id)
      .order_by(AuditLog.created_at.desc())
      .offset(offset)
      .limit(size)
    )).scalars().all()
    total=(await self.db.execute(
      select(func.count(AuditLog.id))
      .where(AuditLog.user_id==user_id)
    )).scalar_one()
    return (list(logs),total)