from typing import Any

from .models import ChatCompletionResponse, InspectResponse
from .transport import AegisTransport


class AegisClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float = 30.0,
    ):
        if not isinstance(api_key, str) or not api_key.strip():
            raise ValueError("api_key must be a non-empty string.")
        if not isinstance(base_url, str) or not base_url.strip():
            raise ValueError("base_url must be a non-empty string.")
        if timeout <= 0:
            raise ValueError("timeout must be greater than 0.")
        
        self._transport = AegisTransport(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
        )

    def inspect(self, prompt: str) -> InspectResponse:
        if not isinstance(prompt,str) or not prompt.strip():
          raise ValueError("prompt must be a non-empty strig.")
        payload = {
            "prompt": prompt,
        }

        data = self._transport.post(
            "chat/inspect",
            payload,
        )

        return InspectResponse.model_validate(data)

    def chat(
        self,
        model: str,
        messages: list[dict[str, Any]],
    ) -> ChatCompletionResponse:
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model must be a non-empty string.")
        if not isinstance(messages, list) or not messages:
            raise ValueError("messages must be a non-empty list.")
        payload = {
            "model": model,
            "messages": messages,
        }

        data = self._transport.post(
            "chat/completions",
            payload,
        )

        return ChatCompletionResponse.model_validate(data)

    def close(self) -> None:
        self._transport.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()