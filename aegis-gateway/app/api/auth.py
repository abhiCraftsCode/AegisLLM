from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import RegisterSchema,AuthResponse,LoginSchema
from app.services.auth import AuthService

auth_router=APIRouter(prefix="/api/auth",tags=["Authentication"])

@auth_router.post("/login",response_model=AuthResponse,status_code=status.HTTP_200_OK)
async def login_user(data:LoginSchema,db:AsyncSession=Depends(get_db)):
  return await AuthService.login_user(data,db)

@auth_router.post("/register",response_model=AuthResponse,status_code=status.HTTP_201_CREATED)
async def register_user(data:RegisterSchema,db:AsyncSession=Depends(get_db)):
  return await AuthService.register_user(data,db)

def is_auth():
  pass