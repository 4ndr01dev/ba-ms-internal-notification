"""
Main configurations and constants for the ETL pipeline.
"""

__all__: list[str] = []

from ..utils.logging import get_logger

_logger = get_logger(__name__)
_default_msg = (
    "Failed to import {module_name}. "
    "See the module's src/configs/__init__.py for more details."
)

try:
    from . import params
    from .params import *  # noqa: F403

    __all__.extend(params.__all__)
except ImportError:
    _logger.warning(_default_msg.format(module_name="params"))

try:
    from . import paths
    from .paths import *  # noqa: F403

    __all__.extend(paths.__all__)
except ImportError:
    _logger.warning(_default_msg.format(module_name="paths"))

try:
    from . import types
    from .types import *  # noqa: F403

    __all__.extend(types.__all__)
except ImportError:
    _logger.warning(_default_msg.format(module_name="types"))
