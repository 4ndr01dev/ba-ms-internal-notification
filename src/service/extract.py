"""
Module to extract data from the source.
"""

__all__ = ["extract_data"]

import json

from ..conn.service_conn import influx_db_service
from ..schemas import ExtractedData, Parameters
from ..utils.logging import get_logger

logger = get_logger(__name__)


def extract_data(params: Parameters) -> ExtractedData:
    """
    Extract data from the source.
    """

    logger.debug("Extracting data from the source...")
    # Inicializar conexión con InfluxDB
    logger.info("Initializing InfluxDB connection...")
    influx_service = influx_db_service()

    # Llamar a la query dummy
    logger.info("Executing dummy query...")
    result = influx_service.query_data_dummy(measurement="alert_metrics")

    # Imprimir el resultado
    logger.info("=" * 60)
    logger.info("QUERY RESULTS:")
    logger.info("=" * 60)
    print("\n" + "=" * 60)
    print("📊 InfluxDB Query Results:")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    print("=" * 60)

    logger.info("No actual alerts will be evaluated or sent.")
    logger.info("=" * 60)

    print("\n✅ Dummy notification executed successfully!\n")
    # TODO: Implement the extraction logic here.

    logger.info("Data extracted successfully.")

    return ExtractedData()
