from __future__ import annotations
from typing import TYPE_CHECKING
from datamodel.soil.SensorReading import SensorReading
import json

if TYPE_CHECKING:
    from database.DBFramework import DBFramework

class Fetch:
    _fw: DBFramework

    def __init__(self, fw_instance: DBFramework) -> None:
        self._fw = fw_instance

    def _get_current_dbs(self) -> None:
        self._tsdb = self._fw.DB.active_tsdb
        self._graphdb = self._fw.DB.active_graphdb

    def complete_model(self) -> list[dict]:
        self._get_current_dbs()

        data = []

        query_data = self._graphdb.run('MATCH (n) RETURN n')
        for obj in query_data:
            node = obj["n"]
            
            if node is None:
                continue

            node = dict(node)['data']
            node = json.loads(str(node))

            if node['object_type'] == 'SOIL:SENSOR_READING':
                reading = SensorReading(json.dumps(node['data']))
                node['data']['values'] = self._tsdb.get_measurement_data(reading)

            data.append(node)
        
        return data
