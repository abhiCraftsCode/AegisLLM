from datetime import datetime
from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ApiKey,AuditLog

class StatReposityory:
  """repository for statistical features"""
  def __init__(self,db:AsyncSession) -> None:
    self.db=db

  # no ruturn type in any method because it is a column-based return
  # and we have always returned eithrer models direclty or none
  # but not particular fields which does not fit in models
  # here we are creating new fields that will always return value

  async def get_log_stats(
      self,
      user_id:int,
      start_date:datetime|None=None,
      end_date:datetime|None=None
    ):
    """fetches the statistical properties of audit-logs"""
    conditions=[AuditLog.user_id==user_id]
    if start_date is not None:
      conditions.append(AuditLog.created_at>=start_date)
    if end_date is not None:
      conditions.append(AuditLog.created_at<=end_date)

    stmt=select(
      func.count(AuditLog.id).label("total_requests"),
      func.count(AuditLog.id)
      .filter(AuditLog.is_blocked.is_(True))
      .label("blocked_requests"),
      func.avg(AuditLog.threat_score).label("avg_threat_score"),
      func.avg(AuditLog.latency_ms).label("avg_latency_ms"),
      func.max(AuditLog.threat_score).label("highest_threat_score")
    ).where(*conditions)

    result=await self.db.execute(stmt)
    return result.one()

  async def get_key_stats(self,user_id:int):
    """fetches stats of api-keys"""
    stmt=select(
      func.count(ApiKey.id).label("total_keys"),
      func.count(ApiKey.id)
      .filter(ApiKey.is_active.is_(True))
      .label("active_keys")
    ).where(ApiKey.user_id==user_id)
    return (await self.db.execute(stmt)).one()

  async def get_activity(
      self,
      user_id:int,
      start_date:datetime|None=None,
      end_date:datetime|None=None
    ):
    """fetches audit-log in time series"""
    stmt=select(
      func.date(AuditLog.created_at).label("date"),
      func.count(AuditLog.id).label("total_requests"),
      func.count(AuditLog.id)
      .filter(AuditLog.is_blocked.is_(True))
      .label("blocked_requests")
    ).where(
      AuditLog.user_id==user_id,
      AuditLog.created_at>=start_date,
      AuditLog.created_at<=end_date
    ).group_by(
      func.date(AuditLog.created_at)
      ).order_by(
        func.date(AuditLog.created_at)
        )

    result=await self.db.execute(stmt)
    return result.all()

  