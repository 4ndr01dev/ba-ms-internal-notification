"""
Module to connect to the service.
"""

__all__: list[str] = []

from ..utils.logging import get_logger

_logger = get_logger(__name__)
_default_msg = (
    "Failed to import {module_name}. "
    "See the module's src/conn/__init__.py for more details."
)

try:
    from . import service_conn
    from .service_conn import *  # noqa: F403

    __all__.extend(service_conn.__all__)
except ImportError:
    _logger.warning(_default_msg.format(module_name="service_conn"))

try:
    from . import token_store_redis
    from .token_store_redis import *  # noqa: F403

    __all__.extend(token_store_redis.__all__)
except ImportError:
    _logger.warning(_default_msg.format(module_name="token_store_redis"))
