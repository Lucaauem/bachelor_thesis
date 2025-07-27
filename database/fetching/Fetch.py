from __future__ import annotations
from typing import TYPE_CHECKING, Any
from datamodel.soil.SensorReading import SensorReading
from database.fetching.FetchStatus import FetchStatus
from database.fetching.FetchOutput import FetchOutput
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

    @staticmethod
    def _output(data: Any, status: FetchStatus) -> dict:
        return {'status':status, 'data':data}
    
    # TODO: Validation
    def _create_output(self, data: Any) -> FetchOutput:
        return FetchOutput(data, FetchStatus.OK)

    def complete_model(self) -> FetchOutput:
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
        
        return self._create_output(data)

    def single_step(self, index:int=-1) -> FetchOutput:
        ...

    def sensor_mea(self, id:str='') -> FetchOutput:
        ...

    def components(self, id:str='', step:str='', shopfloor:str='', include_mea:bool=False) -> FetchOutput:
        ...

    def products(self, step:str='', include_specification:bool=False) -> FetchOutput:
        ...

    def batches(self, index:int=-1) -> FetchOutput:
        ...

    def invalid_datasets(self, include_components:bool=True, include_sensors:bool=True, limit:int=-1) -> FetchOutput:
        ...

    def virtual_sensors(self, sensor:str='', step:str='') -> FetchOutput:
        ...