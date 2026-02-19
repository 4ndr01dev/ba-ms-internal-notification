"""
Module for notification operations.
"""

from ..conn.slack_connection import slack_service

__all__ = ["dummy_notify"]


from ..utils.logging import get_logger

logger = get_logger(__name__)


def dummy_notify() -> None:
    """
    Dummy notification function for testing purposes.
    Initializes InfluxDB connection and queries dummy data.
    """
    slack_service_instance = slack_service()
    slack_service_instance.send_message(
        channel="#general",
        message="This is a dummy notification from the ba-ms-internal-notification service.",
    )
    logger.info("=" * 60)
    logger.info("DUMMY NOTIFICATION EXECUTION")
    logger.info("=" * 60)
