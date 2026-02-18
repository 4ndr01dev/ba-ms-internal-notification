"""
Module for notification operations.
"""

__all__ = ["dummy_notify"]

from ..utils.logging import get_logger

logger = get_logger(__name__)


def dummy_notify() -> None:
    """
    Dummy notification function for testing purposes.
    Prints a message to the console.
    """
    logger.info("=" * 60)
    logger.info("DUMMY NOTIFICATION EXECUTION")
    logger.info("=" * 60)
    logger.info("This is a test notification.")
    logger.info("No actual alerts will be evaluated or sent.")
    logger.info("=" * 60)

    print("\n✅ Dummy notification executed successfully!\n")
