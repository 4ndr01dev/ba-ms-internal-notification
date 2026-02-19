"""
Module for notification operations.
"""

__all__ = ["dummy_notify"]

import json

from ..conn.service_conn import InfluxDBService
from ..utils.logging import get_logger

logger = get_logger(__name__)


def dummy_notify() -> None:
    """
    Dummy notification function for testing purposes.
    Initializes InfluxDB connection and queries dummy data.
    """
    logger.info("=" * 60)
    logger.info("DUMMY NOTIFICATION EXECUTION")
    logger.info("=" * 60)

    # Inicializar conexión con InfluxDB
    logger.info("Initializing InfluxDB connection...")
    influx_service = InfluxDBService()

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
