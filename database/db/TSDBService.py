from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.bucket_api import BucketsApi
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

    def add_measurement(self, measurement: SensorReading) -> None:
        assert self._client is not None
        point = Point(measurement.uuid).time(measurement.timestamp)

        # TODO Check if list in list is possible
        for i, val in enumerate(measurement.value):
            point.field(f"value_{i}", val)

        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self._DATA_BUCKET, org=self._org, record=point)