from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.api.deps import get_current_user
from app.api.deps import get_db
from app.modules.key.service import KeyService
from app.modules.key.schemas import (
  GenerateResponse,
  GenerateSchema,
  KeySchema,
  UpstreamConfig
)

key_router=APIRouter(prefix="/api-keys",tags=["API Keys"])

@key_router.patch("/{key_id}/update",response_model=KeySchema,status_code=status.HTTP_200_OK)
async def update_key(
  key_id:int,
  data:UpstreamConfig,
  user:User=Depends(get_current_user),
  db:AsyncSession=Depends(get_db)
  ):
  """key update request"""
  return await KeyService.update(key_id,user.id,data,db)

@key_router.post("/generate",response_model=GenerateResponse,status_code=status.HTTP_201_CREATED)
async def generate(data:GenerateSchema,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
  """key generation request"""
  return await KeyService.generate_key(data,user.id,db)

@key_router.post("{key_id}/deactivate",response_model=None,status_code=status.HTTP_204_NO_CONTENT)
async def deactivate(key_id:int,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
  """request to deactivate key"""
  await KeyService.deactivate_key(key_id,user.id,db)

@key_router.get("/all",response_model=list[KeySchema],status_code=status.HTTP_200_OK)
async def get_all_keys(user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
  """request for all the keys of user"""
  return await KeyService.get_all_keys(user.id,db)

@key_router.get("/{key_id}",response_model=KeySchema,status_code=status.HTTP_200_OK)
async def get_key(key_id:int,user:User=Depends(get_current_user),db:AsyncSession=Depends(get_db)):
  """single key request"""
  return await KeyService.get_key(key_id,user.id,db)


