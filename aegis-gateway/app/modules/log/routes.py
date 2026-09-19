from fastapi import Depends,APIRouter,status,Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.log.service import LogService
from app.modules.log.schemas import LogSchema,PageResponse
from app.models import User
from app.api.deps import get_db
from app.api.deps import get_current_user

log_router=APIRouter(prefix="/audit-logs",tags=["Audit Log"])

@log_router.get("/all",response_model=PageResponse[LogSchema],status_code=status.HTTP_200_OK)
async def get_logs(
  page:int=Query(default=1,ge=1),
  size:int=Query(default=20,ge=1,le=100),
  user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
  """request to fetch all the log records"""
  return LogService.get_all_logs(user.id,page,size,db)

@log_router.get("/{log_id}",response_model=LogSchema,status_code=status.HTTP_200_OK)
async def get_log(log_id:int,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
  """ request to fetch a log record"""
  return LogService.get_log(log_id,user.id,db)