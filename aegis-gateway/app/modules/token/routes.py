from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.modules.token.schemas import TokenSchema
from app.modules.token.service import TokenService

token_router=APIRouter(prefix="/tokens",tags=["Tokens"])

@token_router.post("/refresh",response_model=TokenSchema,status_code=status.HTTP_201_CREATED)
async def refresh_tokens(db:AsyncSession=Depends(get_db)):
  """to implement refresh token logic but for now s"""
  pass