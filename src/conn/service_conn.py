"""
Module to connect to the service.
"""

__all__ = [
    "JWT_OPTIONAL_TOKEN_PREFIX",
    "extract_payload_from_jwt",
    "CloudRunService",
]

from collections.abc import Callable

import requests  # type: ignore

from ..utils.logging import get_logger

logger = get_logger(__name__)

JWT_OPTIONAL_TOKEN_PREFIX = "x-apigateway-api-userinfo"


def extract_payload_from_jwt(token: str) -> str:
    """
    Extract the encoded payload from a JWT.
    """
    return token.split(".")[1]


class CloudRunService:
    def __init__(self, service_url: str):
        self._service_url = service_url

    def get_token(self) -> str:
        """Get a token for the service."""
        import google.auth.transport.requests as g_auth_req  # type: ignore # noqa: PLC0415
        import google.oauth2.id_token as g_oauth2_id_token  # type: ignore # noqa: PLC0415

        auth_req = g_auth_req.Request()
        target_audience = self._service_url
        id_token = g_oauth2_id_token.fetch_id_token(auth_req, target_audience)
        return id_token  # type: ignore

    def _call_op(self, op: Callable, path: str, **kwargs) -> requests.Response:
        if "headers" in kwargs:
            kwargs["headers"]["Authorization"] = f"Bearer {self.get_token()}"
        else:
            kwargs["headers"] = dict(Authorization=f"Bearer {self.get_token()}")

        return op(self._service_url + path, **kwargs)

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._call_op(requests.get, path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._call_op(requests.post, path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._call_op(requests.delete, path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self._call_op(requests.patch, path, **kwargs)
