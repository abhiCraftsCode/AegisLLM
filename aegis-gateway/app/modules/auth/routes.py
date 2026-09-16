from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.modules.auth.schemas import (
  RegisterSchema,
  AuthResponse,
  LoginSchema,
  TokenSchema,
  ProfileSchema
)
from app.modules.auth.service import AuthService
from app.api.deps import get_current_user
from app.models.user import User

auth_router=APIRouter(prefix="/auth",tags=["Authentication"])

@auth_router.post("/login",response_model=AuthResponse,status_code=status.HTTP_200_OK)
async def login_user(data:LoginSchema,db:AsyncSession=Depends(get_db)):
  """login request by user"""
  return await AuthService.login_user(data,db)

@auth_router.post("/register",response_model=AuthResponse,status_code=status.HTTP_201_CREATED)
async def register_user(data:RegisterSchema,db:AsyncSession=Depends(get_db)):
  """new user signin request"""
  return await AuthService.register_user(data,db)

@auth_router.get("/me",response_model=ProfileSchema,status_code=status.HTTP_200_OK)
def get_profile(current_user:User=Depends(get_current_user)):
  """get current user profile"""
  return ProfileSchema.model_validate(current_user)

@auth_router.post("/refresh",response_model=TokenSchema,status_code=status.HTTP_201_CREATED)
async def refresh_tokens(db:AsyncSession=Depends(get_db)):
  """to implement refresh token logic but for now s"""
  pass