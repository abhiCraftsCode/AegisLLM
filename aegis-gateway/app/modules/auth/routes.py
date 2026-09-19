from fastapi import APIRouter,Depends,status,BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.modules.auth.schemas import (
  RegisterSchema,
  AuthResponse,
  LoginSchema,
  ForgotSchema,
  ResetSchema
)

from app.modules.auth.service import AuthService

auth_router=APIRouter(prefix="/auth",tags=["Authentication"])

@auth_router.post("/login",response_model=AuthResponse,status_code=status.HTTP_200_OK)
async def login_user(data:LoginSchema,db:AsyncSession=Depends(get_db)):
  """login request by user"""
  return await AuthService.login_user(data,db)

@auth_router.post("/register",response_model=AuthResponse,status_code=status.HTTP_201_CREATED)
async def register_user(data:RegisterSchema,db:AsyncSession=Depends(get_db)):
  """new user signin request"""
  return await AuthService.register_user(data,db)

@auth_router.post("/forgot-password",response_model=None,status_code=status.HTTP_204_NO_CONTENT)
async def forgot(data:ForgotSchema,bgt:BackgroundTasks,db:AsyncSession=Depends(get_db)):
  await AuthService.forgot_request(data,bgt,db)

@auth_router.post("/reset-password",response_model=None,status_code=status.HTTP_204_NO_CONTENT)
async def reset(data:ResetSchema,db:AsyncSession=Depends(get_db)):
  await AuthService.reset_request(data,db)