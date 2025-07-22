from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.bucket_api import BucketsApi
from datamodel.soil.SensorReading import SensorReading

class TSDBService():
    _DATA_BUCKET = 'sensor_data'

    _client: InfluxDBClient
    _org: str

    def __init__(self, url: str, token: str, org: str) -> None:
        client = InfluxDBClient(url=url, token=token, org=org)
        self._client = client
        self._org = org

        if not client.buckets_api().find_bucket_by_name(self._DATA_BUCKET):
            client.buckets_api().create_bucket(bucket_name=self._DATA_BUCKET, org=org)

    def add_measurement(self, measurement: SensorReading) -> None:
        point = Point(measurement.uuid).time(measurement.timestamp)

        # TODO Check if list in list is possible
        for i, val in enumerate(measurement.value):
            point.field(f"value_{i}", val)

        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=self._DATA_BUCKET, org=self._org, record=point)