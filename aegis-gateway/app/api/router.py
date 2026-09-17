from fastapi import APIRouter
from app.modules.auth.routes import auth_router
from app.modules.user.routes import user_router
from app.modules.token.routes import token_router
from app.modules.key.routes import key_router

api_router=APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(token_router)
api_router.include_router(key_router)