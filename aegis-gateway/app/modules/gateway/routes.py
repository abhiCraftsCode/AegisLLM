from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.gateway.schemas import (
  InspectRequest,
  InspectResponse,
  ChatCompletionResponse,
  ChatCompletionRequest
)
from app.modules.key.schemas import KeySchema
from app.api.deps import get_current_api_key,get_engine,get_db
from app.core.engine import SecurityEngine
from app.modules.gateway.service import GatewayService

gateway_router=APIRouter(prefix="/chat",tags=["Gateway"])

@gateway_router.post("/inspect",response_model=InspectResponse,status_code=status.HTTP_200_OK)
async def inspect(
  data:InspectRequest,
  key:KeySchema=Depends(get_current_api_key),
  db:AsyncSession=Depends(get_db),
  eng:SecurityEngine=Depends(get_engine)
  ):
  return await GatewayService.inspect(data.prompt,key,eng,db)


@gateway_router.post(
  "/completions",
  response_model=ChatCompletionResponse,
  status_code=status.HTTP_200_OK
  )
async def chat_completion(
  data:ChatCompletionRequest,
  key:KeySchema=Depends(get_current_api_key),
  eng:SecurityEngine=Depends(get_engine),
  db:AsyncSession=Depends(get_db)
):
  return await GatewayService.chat_completion(data,key,eng,db)