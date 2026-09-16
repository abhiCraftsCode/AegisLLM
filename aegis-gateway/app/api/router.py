from fastapi import APIRouter
from app.modules.auth.routes import auth_router
from app.modules.user.routes import user_router

api_router=APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(user_router)