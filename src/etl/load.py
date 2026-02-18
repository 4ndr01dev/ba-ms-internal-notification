"""
Module to load data into the target.
"""

__all__ = ["load_data"]

from ..schemas import Parameters, TransformedData
from ..utils.logging import get_logger

log = get_logger(__name__)


def load_data(data: TransformedData, params: Parameters):
    """
    Load data into the target.
    """
    log.debug("Loading data into the target...")

    # TODO: Implement the loading logic here.

    log.info("Data loaded successfully.")
