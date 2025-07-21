from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS

class TSDBService():
    _client: InfluxDBClient

    def __init__(self, url: str, token: str, org: str) -> None:
        client = InfluxDBClient(url=url, token=token, org=org)
        self._client = client

    def write(self):
        ...