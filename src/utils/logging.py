"""
Module to handle logging with rich and cloud logging.
"""

from __future__ import annotations

import logging as _logging
import os
import typing as t
from functools import wraps

__all__ = [
    "get_logger",
    "check_if_any_logger_is_below_level",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "LOG_LEVELS",
]

DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50


__LEVEL_MAP = {
    "DEBUG": DEBUG,
    DEBUG: DEBUG,
    "INFO": INFO,
    INFO: INFO,
    "WARNING": WARNING,
    WARNING: WARNING,
    "ERROR": ERROR,
    ERROR: ERROR,
    "CRITICAL": CRITICAL,
    CRITICAL: CRITICAL,
}
"""
The mapping of level names to their corresponding integer values.
"""

LOG_LEVELS = [lvl for lvl in __LEVEL_MAP.keys() if isinstance(lvl, str)]


class _HandlerManager:
    """
    Class to create and manage handlers for the logger. Just call the
    `get_handler_from_env` method to get the handler from the
    environment variable `LOGGING_HANDLER`.

    The class has a default handler that is used if the handler is not
    found. The default handler is a stream handler that logs to the
    console. Its format is in the `DEFAULT_FMT` class attribute.

    If you want to add a new handler, you can add a method to the class
    that starts with `get_` and ends with `_handler`. For example:
    - `get_cloud_handler` -> `'cloud'`
    - `get_rich_handler` -> `'rich'`
    - `get_default_handler` -> `'default'`
    """

    type DefaultHandler = _logging.StreamHandler[t.TextIO]

    DEFAULT_FMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    """
    The default format for the default logger.
    """

    DEFAULT_HANDLER_TYPE = "rich"
    """
    The default handler type to use if the environment variable
    `LOGGING_HANDLER` is not set.
    """

    _warning_shown: bool = False
    _current_handler_type: str = "default"

    # === GET HANDLER FROM ENVIRONMENT VARIABLE ===
    @classmethod
    def get_handler_from_env(cls) -> _logging.Handler:
        """
        Get a handler for the logger from the environment variable
        `LOGGING_HANDLER`. If the environment variable is not set,
        the default handler type is used.

        Raises a ValueError if the handler type is invalid.
        """
        handler_funcs = cls.get_handler_funcs()

        handler_type = os.getenv("LOGGING_HANDLER", cls.DEFAULT_HANDLER_TYPE)
        handler_type = handler_type.lower()

        if handler_type not in handler_funcs:
            valid_handlers = map(repr, handler_funcs.keys())
            raise ValueError(
                f"Invalid LOGGING_HANDLER={repr(handler_type)}. "
                f"Valid handlers are: {', '.join(valid_handlers)}."
            )

        cls._current_handler_type = handler_type

        handler_func = handler_funcs[handler_type]
        return handler_func()

    # === DEFAULT HANDLER ===
    @classmethod
    def get_default_handler(cls) -> DefaultHandler:
        """
        Get the default handler for the logger.
        """
        handler = _logging.StreamHandler()
        formatter = _logging.Formatter(cls.DEFAULT_FMT)
        handler.setFormatter(formatter)

        return handler

    @staticmethod
    def safe_handler_setting[**P, R: _logging.Handler](
        func: t.Callable[t.Concatenate[type[t.Self], P], R],
    ) -> t.Callable[
        t.Concatenate[type[t.Self], P],
        R | _HandlerManager.DefaultHandler,
    ]:
        """
        Decorator to safely set a handler for the logger.

        If during the execution of the function an exception is raised,
        the default handler will be used.

        The decorator assumes that the method to decorate is a class
        method.
        """

        @wraps(func)
        def wrapper(
            cls: type[_HandlerManager], *args: P.args, **kwargs: P.kwargs
        ) -> R | _HandlerManager.DefaultHandler:

            log = _logging.getLogger("ba.logging")
            log.addHandler(cls.get_default_handler())
            try:
                return func(cls, *args, **kwargs)

            except ModuleNotFoundError:
                if not cls._warning_shown:
                    log.warning(
                        "Failed to import the "
                        f"{repr(cls._current_handler_type)} handler. "
                        "Using the default handler."
                    )
                    cls._warning_shown = True
                return cls.get_default_handler()

            except Exception as e:
                raise Exception(f"Error setting up handler: {e}") from e

        return wrapper

    # === GET OTHER HANDLERS ===
    @classmethod
    @safe_handler_setting
    def get_rich_handler(cls: type[t.Self]):
        """
        Get the rich handler for the logger.
        """
        import rich.logging  # type: ignore # noqa: PLC0415

        return rich.logging.RichHandler()

    @classmethod
    @safe_handler_setting
    def get_cloud_handler(cls: type[t.Self]):
        """
        Get the cloud logging handler for the logger.
        """
        import google.cloud.logging as gc_log  # type: ignore # noqa: PLC0415

        client = gc_log.Client()
        return gc_log.handlers.CloudLoggingHandler(client)

    # === GET ALL HANDLER FUNCTIONS ===
    @classmethod
    def get_handler_funcs(cls) -> dict[str, t.Callable[[], _logging.Handler]]:
        """
        The functions to get the handlers. Automatically discovers
        handler methods by inspecting class methods that start with
        `get_` and end with `_handler`.

        The key is extracted from the method name by removing `get_`
        prefix and `_handler` suffix. For example:
        - `get_cloud_handler` -> `'cloud'`
        - `get_rich_handler` -> `'rich'`
        - `get_default_handler` -> `'default'`
        """
        handler_funcs: dict[str, t.Callable[[], _logging.Handler]] = {}

        # Get all attributes of the class
        for name in dir(cls):
            # Check if attribute follows the pattern get_*_handler
            if not (name.startswith("get_") and name.endswith("_handler")):
                continue

            handler_func: t.Callable[[], _logging.Handler] = getattr(cls, name)
            # Check if it's callable (a method)
            if not callable(handler_func):
                continue

            # Remove 'get_' (4 chars) and '_handler' (8 chars)
            key = name[4:-8]
            handler_funcs[key] = handler_func

        return handler_funcs


def _get_level(level: str | int | None, default: int = INFO) -> int:
    """
    Get the level of the logger from a string or integer.

    If the level is not provided, return the default level.
    If the level is not valid, raise a ValueError.
    """
    if level is None:
        return default

    level = level.upper() if isinstance(level, str) else level
    if level not in __LEVEL_MAP:
        raise ValueError(
            f"Invalid level: {repr(level)}. "
            f"Valid levels are: {', '.join(map(repr, LOG_LEVELS))}."
        )

    return __LEVEL_MAP[level]


def get_logger(
    name: str,
    level: str | int | None = None,
    handler: _logging.Handler | None = None,
) -> _logging.Logger:
    """
    Get a logger with the given name and level. If the logger already
    exists, set the level and handler if provided. Otherwise, create a
    new logger with the given name and level.

    Parameters
    ----------
    name : str
        The name of the logger.
    level : int | None, optional
        The level of the logger. If None, the level will be set to INFO.
    handler : logging.Handler | None, optional
        The handler to add to the logger. If None, the handler will be
        set to the handler from the environment variable
        `LOGGING_HANDLER`. If the environment variable is not set, the
        default handler will be used.

    Returns
    -------
    Logger
        The logger.
    """

    # === GET LOGGER IF IT EXISTS ===
    # If the logger already exists, set the level and handler if provided
    if name in _logging.Logger.manager.loggerDict:
        logger = _logging.getLogger(name)
        if level is not None:
            logger.setLevel(level)
        if handler is not None:
            logger.addHandler(handler)
        return logger

    # === CREATE LOGGER IF IT DOES NOT EXIST ===
    logger = _logging.getLogger(name)

    # === SET LEVEL ===
    # Set the level of the logger. If no level is provided, set it to INFO.
    logger.setLevel(_get_level(level))

    # === ADD HANDLER IF IT IS PROVIDED ===
    # If a handler is provided, add it to the logger and return the logger
    if handler is not None:
        logger.addHandler(handler)
        return logger

    # === SET HANDLER IF IT IS NOT PROVIDED ===
    handler = _HandlerManager.get_handler_from_env()
    logger.addHandler(handler)

    return logger


def check_if_any_logger_is_below_level(max_level: int | str = INFO) -> bool:
    """
    Check if any logger is below the given level.
    """

    logger = get_logger(__name__)

    is_any_logger_below_level = False

    for logger_name, logger in _logging.Logger.manager.loggerDict.items():
        if not isinstance(logger, _logging.Logger):
            continue

        # Skip non-src loggers. (e.g. rich or dotenv.main...)
        if "src" not in logger_name:
            continue

        max_level_int = _get_level(max_level)

        if logger.level and logger.level < max_level_int:
            logger.warning(
                f"Logger '{logger_name}' is in level {logger.level}."
            )
            is_any_logger_below_level = True

    return is_any_logger_below_level
