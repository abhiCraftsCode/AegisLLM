from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.user.schemas import ProfileSchema,UpdateSchema,PasswordSchema
from app.modules.user.service import UserService
from app.api.deps import get_current_user,get_db

user_router=APIRouter(prefix="/users",tags=["User"])

@user_router.get("/me",response_model=ProfileSchema,status_code=status.HTTP_200_OK)
def get_profile(current_user:ProfileSchema=Depends(get_current_user)):
  """get current user profile"""
  return current_user

@user_router.patch(
    "/update/profile",
    response_model=ProfileSchema,
    status_code=status.HTTP_200_OK
    )
async def update(
  data:UpdateSchema,
  user:ProfileSchema=Depends(get_current_user),
  db:AsyncSession=Depends(get_db)
  ):
  """request to update profile."""
  return await UserService.update(data,user.id,db)

@user_router.put("/update",response_model=None,status_code=status.HTTP_204_NO_CONTENT)
async def password(
  data:PasswordSchema,
  user:ProfileSchema=Depends(get_current_user),
  db:AsyncSession=Depends(get_db)):
  await UserService.password_update(data,user.id,db)
