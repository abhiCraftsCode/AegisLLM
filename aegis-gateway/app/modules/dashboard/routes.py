from fastapi import APIRouter,Depends,status,Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal
from datetime import date

from app.api.deps import get_current_user,get_db
from app.modules.dashboard.service import StatService
from app.modules.user.schemas import ProfileSchema
from app.modules.dashboard.schemas import StatSchema

stat_router=APIRouter(prefix="/dashboard",tags=["Dashboard"])

@stat_router.get("/stats",response_model=StatSchema,status_code=status.HTTP_201_CREATED)
async def get_stat(
  user:ProfileSchema=Depends(get_current_user),
  db:AsyncSession=Depends(get_db),
  period:Literal["lifetime","monthly","range"]="lifetime",
  month:int|None=Query(default=None),
  year:int|None=Query(default=None),
  to_date:date|None=Query(default=None),
  from_date:date|None=Query(default=None)
  ):
  """request to generate stats for the dashboard"""
  return await StatService.get_stats(
    user.id,db,period,year,month,to_date,from_date
    )