import httpx
from typing import Any

from .errors import (
    AegisAuthenticationError,
    AegisGatewayError,
    AegisError,
    AegisRateLimitError,
)


class AegisTransport:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(
            timeout=timeout,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )

    def post(
        self,
        path: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
      try:
        response = self.client.post(
            f"{self.base_url}/{path.lstrip('/')}",
            json=payload,
        )
      except httpx.TimeoutException as exc :
        raise AegisGatewayError("Request to Aegis timed out.") from exc
      except httpx.RequestError as exc:
        raise AegisGatewayError("Unable to connect to Aegis-gateway.") from exc
      
      self._handle_error(response)
      
      try:
        return response.json()
      except ValueError as exc:
        raise AegisError(
            "Aegis returned an invalid response."
        ) from exc

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code<400:
          return 
        detail = self._get_error_detail(response)
        status_code=response.status_code
        if status_code in (401, 403):
            raise AegisAuthenticationError(
                detail,
                status_code,
            )

        if status_code == 429:
            raise AegisRateLimitError(
                detail,
                status_code,
            )

        if status_code in (502, 504):
            raise AegisGatewayError(
                detail,
                status_code,
            )

        raise AegisError(
            detail,
            status_code,
        )
    
    def close(self) -> None:
        self.client.close()
    
    @staticmethod
    def _get_error_detail(
        response: httpx.Response,
    ) -> str:
        try:
            data = response.json()
            if isinstance(data, dict):
                detail = data.get("detail")
                if isinstance(detail, str) and detail:
                    return detail
        except ValueError:
            pass
        return f"Aegis request failed with status {response.status_code}."
    