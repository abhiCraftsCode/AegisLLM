from fastapi import APIRouter,Depends,status
from app.modules.user.schemas import ProfileSchema
from app.api.deps import get_current_user
from app.models import User

user_router=APIRouter(prefix="/users")

@user_router.get("/me",response_model=ProfileSchema,status_code=status.HTTP_200_OK)
def get_profile(current_user:User=Depends(get_current_user)):
  """get current user profile"""
  return ProfileSchema.model_validate(current_user)
