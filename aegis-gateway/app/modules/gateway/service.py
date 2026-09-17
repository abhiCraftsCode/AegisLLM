import httpx
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.engine import SecurityEngine
from app.modules.log.service import LogService
from app.modules.key.service import KeyService
from app.models import AuditLog
from app.modules.gateway.schemas import (
  InspectResponse,
  ChatCompletionRequest,
  ChatCompletionResponse
)
from app.modules.key.schemas import KeySchema

class GatewayService:
  """services related to the proxy gateway"""

  @staticmethod
  async def inspect(
    prompt:str,
    key:KeySchema,
    eng:SecurityEngine,
    db:AsyncSession
    )->InspectResponse:
    """inspect prompt and audit respective log"""
    request_id=uuid4()

    result=await eng.inspect(prompt)

    audit_log = AuditLog(
        request_id=request_id,
        user_id=key.user_id,
        key_id=key.id,
        threat_score=result.threat_score,
        is_blocked=result.is_blocked,
        reason=result.reason,
        latency=result.latency_ms
    )
    log=await LogService.create_log(audit_log,db)

    return InspectResponse.model_validate(log)

  @staticmethod
  async def chat_completion(
    data:ChatCompletionRequest,
    key:KeySchema,
    eng:SecurityEngine,
    db:AsyncSession
    )->ChatCompletionResponse:
    """request to inspect and upstream prompt"""

    # check for llm credentials availability
    config=await KeyService.get_llm_config(key.id,db)
    request_id=uuid4()
    usr_msg=[message.content for message in data.messages if message.role=="user"]
    prompt="\n".join(usr_msg)

    result=await eng.inspect(prompt)

    audit_log = AuditLog(
        request_id=request_id,
        user_id=key.user_id,
        key_id=key.id,
        threat_score=result.threat_score,
        is_blocked=result.is_blocked,
        reason=result.reason,
        latency=result.latency_ms,
        llm_name=key.llm_name,
        llm_url=config.llm_url
    )
    log=await LogService.create_log(audit_log,db)

    if result.is_blocked:
      return ChatCompletionResponse.model_validate(log)

    async with httpx.AsyncClient(timeout=30.0) as client:
      res=await client.post(
        config.llm_url,
        headers={"Authorization":f"Bearer {config.llm_url}"},
        json={"prompt":prompt}
      )

    return ChatCompletionResponse.model_validate(res)

  