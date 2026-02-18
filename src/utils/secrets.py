"""
Module to handle secrets management.
"""

__all__ = [
    "safe_get_env",
    "get_secret",
    "load_custom_dotenv",
]

import os
from typing import IO

from .logging import get_logger

logger = get_logger(__name__)


def safe_get_env(key: str, default: str | None = None) -> str:
    """
    Safely get an environment variable.
    Raise an exception if it is not found and no default is provided.
    """
    var = os.getenv(key.upper(), default)

    if var is None:
        msg = f"Environment variable '{key}' is not set"
        logger.error(msg)
        raise ValueError(msg)

    logger.debug(f"Getting environment variable: '{key}'")

    return var


def get_secret(secret_name: str, project_id: str) -> str:
    """Fetches a secret from Google Secret Manager."""
    from google.cloud import secretmanager  # type: ignore # noqa: PLC0415

    logger.debug(f"Getting secret: '{secret_name}'")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    try:
        response = client.access_secret_version(request={"name": name})
        logger.debug(f"Successfully fetched secret: '{secret_name}'")
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(
            f"Error accessing secret '{secret_name}': {e}",
            exc_info=True,
        )
        raise e


def load_custom_dotenv(  # noqa: PLR0913
    dotenv_path: os.PathLike[str] | str | None = None,
    stream: IO[str] | None = None,
    verbose: bool = True,
    override: bool = True,
    interpolate: bool = True,
    encoding: str | None = "utf-8",
) -> None:
    """
    Load environment variables from a .env file. If the file is not found,
    the function will not raise an error.

    for more information, see the documentation of the dotenv library:
    https://saurabh-kumar.com/python-dotenv/
    """
    try:
        from dotenv import load_dotenv  # type: ignore # noqa: PLC0415

        load_dotenv(
            dotenv_path=dotenv_path,
            stream=stream,
            verbose=verbose,
            override=override,
            interpolate=interpolate,
            encoding=encoding,
        )
        logger.info(f"Loaded environment variables from {repr(dotenv_path)}.")

    except ImportError:
        logger.warning(
            "dotenv not installed. Skipping environment variable loading... "
            "(expected in cloud environment)."
        )

    except Exception as e:
        logger.error(f"Error loading environment variables: {e}", exc_info=True)
        raise e
