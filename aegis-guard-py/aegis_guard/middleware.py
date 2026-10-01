from langchain.agents.middleware import AgentMiddleware, ModelRequest, ModelResponse
from langchain_core.messages import AIMessage

from aegis_guard import AegisClient


class AegisMiddleware(AgentMiddleware):
    def __init__(self, api_key: str, base_url: str):
        super().__init__()
        self.client = AegisClient(
            api_key=api_key,
            base_url=base_url,
        )

    def wrap_model_call(self, request: ModelRequest, handler):
        messages = request.state.get("messages", [])

        if not messages:
            return handler(request)

        last_message = messages[-1]

        if getattr(last_message, "type", None) != "human":
            return handler(request)

        content = last_message.content

        if not isinstance(content, str):
            return handler(request)

        result = self.client.inspect(content)

        if result.is_blocked:
            return ModelResponse(
                result=[
                    AIMessage(
                        content="Request blocked by AegisLLM."
                    )
                ]
            )

        return handler(request)