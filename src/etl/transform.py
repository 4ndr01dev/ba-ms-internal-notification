"""
Module to transform data.
"""

__all__ = ["transform_data"]

from ..schemas import ExtractedData, Parameters, TransformedData
from ..utils.logging import get_logger

logger = get_logger(__name__)


def transform_data(data: ExtractedData, params: Parameters) -> TransformedData:
    """
    Transform data.
    """
    logger.debug("Transforming data...")

    # TODO: Implement the transformation logic here.

    logger.info("Data transformed successfully.")

    return TransformedData()
