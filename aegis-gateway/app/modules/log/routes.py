from fastapi import Depends,APIRouter,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.log.service import LogService
from app.models import User
from app.db.session import get_db
from app.api.deps import get_current_user

log_router=APIRouter(prefix="/audit-logs",tags=["Audit Log"])

@log_router.get("/all")
async def get_logs(user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
  return LogService.get_all_logs(user.id,db)

@log_router.get("/{log_id}")
async def get_log(log_id:int,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
  return LogService.get_log(log_id,user.id,db)