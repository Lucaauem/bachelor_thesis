from __future__ import annotations
from typing import TYPE_CHECKING
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.bucket_api import BucketsApi
from datamodel.soil.SensorReading import SensorReading
from datetime import datetime, timezone, timedelta

if TYPE_CHECKING:
    from datamodel.soil.SensorReading import SensorReading

class TSDBService():
    _DATA_BUCKET = 'sensor_data'

    _url: str
    _token: str
    _org: str
    _client: InfluxDBClient | None = None

    def __init__(self, url: str, token: str, org: str) -> None:
        self._url = url
        self._token = token
        self._org = org

    def connect(self) -> None:
        assert self._client is None
        client = InfluxDBClient(url=self._url, token=self._token, org=self._org)
        self._client = client

        if not client.buckets_api().find_bucket_by_name(self._DATA_BUCKET):
            client.buckets_api().create_bucket(bucket_name=self._DATA_BUCKET, org=self._org)

    def disconnect(self) -> None:
        assert self._client is not None
        self._client.close()

    @staticmethod
    def _create_timestamp(timestamp: str) -> datetime:
        dt = datetime.fromisoformat(timestamp)
        dt_utc = datetime.fromtimestamp(dt.timestamp(), tz=timezone.utc)
        return dt_utc

    def add_measurement(self, uuid:str, timestamp: str, value: list) -> None:
        assert self._client is not None
        point = Point('sensor_reading').tag('uuid', uuid).time(TSDBService._create_timestamp(timestamp))

        # TODO Check if list in list is possible
        for i, val in enumerate(value):
            point.field(f"value_{i}", val)

        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self._DATA_BUCKET, org=self._org, record=point)

    def get_measurement_data(self, reading: SensorReading) -> list:
        assert self._client is not None

        # Convert timestamp time to UTC
        timestamp = TSDBService._create_timestamp(reading.timestamp)

        # +-100 ms
        delta = timedelta(milliseconds=100)
        start = (timestamp - delta).isoformat()
        stop = (timestamp + delta).isoformat()

        query = f'''
            from(bucket: "{self._DATA_BUCKET}")
            |> range(start: {start}, stop: {stop})
            |> filter(fn: (r) => r._measurement == "sensor_reading")
            |> filter(fn: (r) => r.uuid == "{reading.uuid}")
            |> sort(columns: ["_time"], desc: false)
            |> limit(n:1)
        '''
        
        query_api = self._client.query_api()
        result = query_api.query(org=self._org, query=query)
        values = []
        for table in result:
            for record in table.records:
                values.append(record.get_value())

        return values