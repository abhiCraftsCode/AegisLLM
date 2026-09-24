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
from app.core.security import decrypt_field
from app.core.exceptions import UpstreamLLMError

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
        latency_ms=result.latency_ms
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
        latency_ms=result.latency_ms,
        llm_name=key.llm_name,
        llm_url=config.llm_url
    )
    #log is being created and committed to db
    # if llm response fails to an error then the log is already commited
    # even though the response was never made
    log=await LogService.create_log(audit_log,db)
    chat_response=ChatCompletionResponse.model_validate(log)
    if result.is_blocked:
      return chat_response
    auth=decrypt_field(config.llm_auth)
    if auth is None: raise #only for safety real error already raised in service
    upstream_paload=data.model_dump()
    # global static nature fetch call 
    # so that every inspect does not create its own upstream call function
    async with httpx.AsyncClient(timeout=30.0) as client:
      res=await client.post(
        config.llm_url,
        headers={
          "Authorization":f"Bearer {auth}",
          "Content-Type":"application/json"
          },
        json=upstream_paload
      )
    if not res.is_success:
      raise UpstreamLLMError()
    
    chat_response.response=res.json()
    return chat_response

  