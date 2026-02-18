"""
Module to store and retrieve tokens from Redis.
"""

__all__ = ["TokenStoreRedis", "get_service_token"]

from datetime import datetime, timedelta
from http import HTTPStatus

import requests  # type: ignore

from ..utils.logging import get_logger
from ..utils.secrets import get_secret, safe_get_env

logger = get_logger(__name__)

Token = str


class TokenStoreRedis:
    """TokenStoreRedis class."""

    def __init__(  # noqa: PLR0913
        self,
        host: str,
        port: int,
        password: str,
        auth0_domain: str,
        auth0_client_id: str,
        auth0_client_secret: str,
        auth0_audience: str,
    ) -> None:
        """Init TokenStoreRedis class.

        Usage:
            >>> token_store = TokenStoreRedis(
            ...     host="localhost",
            ...     port=6379,
            ...     password="",
            ...     auth0_domain="https://mydomain.eu.auth0.com",
            ...     auth0_client_id="my_client_id",
            ...     auth0_client_secret="my_client_secret",
            ...     auth0_audience="https://mydomain.eu.auth0.com/api/v2/",
            ... )
            >>> token = token_store()

        Args:
            host (str): Redis host.
            port (int): Redis port.
            password (str): Redis password.
            auth0_domain (str): Auth0 domain.
            auth0_client_id (str): Auth0 client id.
            auth0_client_secret (str): Auth0 client secret.
            auth0_audience (str): Auth0 audience.
        """

        import redis  # type: ignore  # noqa: PLC0415

        self.__client: redis.StrictRedis = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            encoding="utf-8",
            decode_responses=True,
        )
        self._auth0_domain = auth0_domain
        self._auth0_client_id = auth0_client_id
        self._auth0_client_secret = auth0_client_secret
        self._auth0_audience = auth0_audience

    def __call__(self) -> str:
        """
        Get token from Redis.

        If token does not exist, get token from Auth0 and store it in Redis.
        If token has expired, get token from Auth0 and store it in Redis.
        """
        import jwt  # type: ignore  # noqa: PLC0415

        # Get token from Redis
        access_token: str | None = self.__client.get(name=self._auth0_client_id)  # type: ignore

        # Check if token exist
        if access_token is None:
            return self._renew_token()

        # Check if token has expired
        jwt_options = {"verify_signature": False}
        jwt_decoded = jwt.decode(access_token, options=jwt_options)
        exp = datetime.fromtimestamp(jwt_decoded["exp"]) - timedelta(minutes=10)
        if datetime.now() > exp:
            return self._renew_token()

        return access_token

    def _renew_token(self) -> str:
        """Renew token in Redis from Auth0."""
        new_token = self._get_token()
        self.__client.set(name=self._auth0_client_id, value=new_token)
        return new_token

    def _get_token(self) -> str:
        """Get token from auth0."""
        res = requests.post(
            self._auth0_domain + "/oauth/token",
            headers={"content-type": "application/json"},
            json={
                "client_id": self._auth0_client_id,
                "client_secret": self._auth0_client_secret,
                "audience": self._auth0_audience,
                "grant_type": "client_credentials",
            },
        )
        if res.status_code != HTTPStatus.OK:
            raise Exception(
                "Error when trying to retrieve the token to access the"
                f" services. status_code={res.status_code}."
                f" detail={res.content!r}"
            )

        return res.json()["access_token"]


def get_service_token() -> Token:
    """
    Get the service token using credentials fetched from Secret Manager.
    Environment variables are expected to be set on the Cloud Run Job.
    """
    logger.debug("Getting service token...")

    gcp_project_id = safe_get_env("GCP_PROJECT_ID")
    auth0_client_secret_key = safe_get_env("AUTH0_CLIENT_SECRET_KEY")
    redis_pass_token_cache_key = safe_get_env("REDIS_PASS_TOKEN_CACHE_KEY")

    auth0_client_secret = get_secret(auth0_client_secret_key, gcp_project_id)
    redis_pass = get_secret(redis_pass_token_cache_key, gcp_project_id)

    token_store = TokenStoreRedis(
        host=safe_get_env("REDIS_HOST_TOKEN_CACHE"),
        port=int(safe_get_env("REDIS_PORT_TOKEN_CACHE")),
        password=redis_pass,
        auth0_domain=safe_get_env("AUTH0_DOMAIN"),
        auth0_client_id=safe_get_env("AUTH0_CLIENT_ID"),
        auth0_client_secret=auth0_client_secret,
        auth0_audience=safe_get_env("AUTH0_AUDIENCE"),
    )
    return token_store()
