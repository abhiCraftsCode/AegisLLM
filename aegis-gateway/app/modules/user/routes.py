from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.schemas import ProfileSchema,UpdateSchema
from app.modules.user.service import UserService
from app.api.deps import get_current_user,get_db

user_router=APIRouter(prefix="/users",tags=["User"])

@user_router.get("/me",response_model=ProfileSchema,status_code=status.HTTP_200_OK)
def get_profile(current_user:ProfileSchema=Depends(get_current_user)):
  """get current user profile"""
  return current_user

@user_router.post("/profile-update",response_model=ProfileSchema,status_code=status.HTTP_200_OK)
async def update(
  data:UpdateSchema,
  user:ProfileSchema=Depends(get_current_user),
  db:AsyncSession=Depends(get_db)
  ):
  """request to update profile."""
  return await UserService.update(data,user.id,db)