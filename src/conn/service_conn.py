"""
Module to connect to InfluxDB service.
"""

__all__ = [
    "InfluxDBService",
]

import os
from typing import Any

from ..utils.logging import get_logger

logger = get_logger(__name__)


class InfluxDBService:
    def __init__(self):
        self._host = os.getenv("INFLUXDB_HOST")
        self._org = os.getenv("INFLUXDB_ORG")
        self._bucket = os.getenv("INFLUXDB_BUCKET")
        self._token_key = os.getenv("INFLUXDB_TOKEN_KEY")

        logger.info(f"InfluxDB Service initialized with host: {self._host}")

    def query_data_dummy(
        self, measurement: str = "test_measurement"
    ) -> dict[str, Any]:
        """
        Dummy function to simulate reading data from InfluxDB.

        Args:
            measurement: The measurement name to query (dummy parameter)

        Returns:
            A dictionary simulating query results from InfluxDB
        """
        logger.info(
            f"Simulating query to InfluxDB - Bucket: {self._bucket}, Measurement: {measurement}"
        )

        # Simulated response
        dummy_data = {
            "status": "success",
            "bucket": self._bucket,
            "org": self._org,
            "measurement": measurement,
            "data": [
                {
                    "time": "2026-02-19T10:00:00Z",
                    "field1": 42.5,
                    "field2": "sample_value",
                    "tag1": "sensor_1",
                },
                {
                    "time": "2026-02-19T10:01:00Z",
                    "field1": 43.2,
                    "field2": "sample_value_2",
                    "tag1": "sensor_1",
                },
            ],
        }

        logger.info(
            f"Query simulation completed. Returned {len(dummy_data['data'])} records"
        )
        return dummy_data
