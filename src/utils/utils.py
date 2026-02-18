"""
Utility functions for the project.
"""

__all__: list[str] = [
    "dump_json",
    "retry",
]


import time
from collections.abc import Callable
from functools import wraps

from ..configs.types import JsonType


def dump_json(data: JsonType) -> str:
    """
    Dump a JSON object to a string. Useful to have a pretty print of a
    JSON or dictionary object.
    """
    import json  # noqa: PLC0415

    return json.dumps(data, indent=4)


def retry(
    retries: int = 3,
    retry_delay_seconds: int = 60,
    callback: Callable[[str], None] = lambda x: None,
):
    """
    Decorator to retry a function a certain number of times with a
    delay between retries.

    Parameters
    ----------
    retries : int, optional
        The number of times to retry the function, by default 3
    retry_delay_seconds : int, optional
        The delay between retries in seconds, by default 60
    callback : Callable[[str], None], optional
        A callback function to be called when an error occurs.
        The function will be called with the error message.

    Returns
    -------
    Callable[[P, R], R]
        The decorated function.
    """

    def decorator[**P, R](func: Callable[P, R]) -> Callable[P, R]:

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for i in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    callback(
                        "An error occurred, "
                        f"retrying again in {retry_delay_seconds} seconds... "
                        f"({i}/{retries}): {e}"
                    )
                    time.sleep(retry_delay_seconds)
                    callback(f"Retrying... ({i}/{retries})")
            callback("Max retries reached, stopping...")
            # TODO: add a custom exception
            raise Exception(f"Max retries reached after {retries} attempts")

        return wrapper

    return decorator
