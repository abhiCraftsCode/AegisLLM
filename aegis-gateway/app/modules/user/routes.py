from fastapi import APIRouter

user_router=APIRouter(prefix="/users")

@user_router.get("/me")
def get_user_profile():
  pass