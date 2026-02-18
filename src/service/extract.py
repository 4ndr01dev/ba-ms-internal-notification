"""
Module to extract data from the source.
"""

__all__ = ["extract_data"]

from ..schemas import ExtractedData, Parameters
from ..utils.logging import get_logger

logger = get_logger(__name__)


def extract_data(params: Parameters) -> ExtractedData:
    """
    Extract data from the source.
    """

    logger.debug("Extracting data from the source...")

    # TODO: Implement the extraction logic here.

    logger.info("Data extracted successfully.")

    return ExtractedData()
