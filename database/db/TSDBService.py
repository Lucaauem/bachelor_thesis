from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datamodel.soil.SensorReading import SensorReading

class TSDBService():
    _client: InfluxDBClient
    _org: str

    def __init__(self, url: str, token: str, org: str) -> None:
        client = InfluxDBClient(url=url, token=token, org=org)
        self._client = client
        self._org = org

    def add_measurement(self, measurement: SensorReading) -> None:
        point = Point(measurement.uuid).time(measurement.timestamp)

        # TODO Check if list in list is possible
        for i, val in enumerate(measurement.value):
            point.field(f"value_{i}", val)

        write_api = self._client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket='soil', org=self._org, record=point)