from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuditLog
from app.modules.log.repostiory import LogRepository
from app.modules.log.schemas import LogSchema
from app.core.exceptions import UnauthorizedUserError,LogNotFoundError

class LogService:
  """provide all services for audit-logs"""

  @staticmethod
  async def create_log(log:AuditLog,db:AsyncSession)->LogSchema:
    """create a new log row"""
    repo=LogRepository(db)
    try:
      log=await repo.create(log)
      await db.commit()
    except Exception:
      await db.rollback()
      raise
    return LogSchema.model_validate(log)

  @staticmethod
  async def get_all_logs(user_id:int,db:AsyncSession)->list[LogSchema]:
    """fetch all the logs of user"""
    repo=LogRepository(db)
    logs=await repo.get_all_for_user(user_id)
    return [LogSchema.model_validate(log) for log in logs]

  @staticmethod
  async def get_log(log_id:int,user_id:int,db:AsyncSession)->LogSchema:
    """fetch a log record"""
    repo=LogRepository(db)
    log=await repo.get_by_id(log_id)
    if log is None:
      raise LogNotFoundError()
    if log.user_id!=user_id:
      raise UnauthorizedUserError()
    return LogSchema.model_validate(log)