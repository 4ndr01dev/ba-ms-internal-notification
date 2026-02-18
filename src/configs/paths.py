"""
Module to handle paths.

The paths are checked to exist at import time.
"""

__all__: list[str] = [
    "CWD_PATH",
    "PROJECT_ROOT_PATH",
]

from pathlib import Path

from ..utils.logging import get_logger

logger = get_logger(__name__)


__all_paths = []

CWD_PATH = Path.cwd()
logger.debug(f"CWD_PATH: {CWD_PATH}")
__all_paths.append(CWD_PATH)

PROJECT_ROOT_PATH = CWD_PATH
logger.debug(f"PROJECT_ROOT_PATH: {PROJECT_ROOT_PATH}")
__all_paths.append(PROJECT_ROOT_PATH)

# === Check if all paths exist ===

for __path in __all_paths:
    if not __path.exists():
        msg = f"Path does not exist: {__path}"
        logger.error(msg)
        raise FileNotFoundError(msg)
