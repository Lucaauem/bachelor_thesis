from __future__ import annotations
from typing import TYPE_CHECKING, Any
from datamodel.soil.SensorReading import SensorReading
from database.fetching.FetchStatus import FetchStatus
from database.fetching.FetchOutput import FetchOutput
from database.DatasetType import DatasetType
import json

if TYPE_CHECKING:
    from database.DBFramework import DBFramework

class Fetch:
    _fw: DBFramework
    _ignores_failed_validation: bool = False

    def __init__(self, fw_instance: DBFramework) -> None:
        self._fw = fw_instance

    def _get_current_dbs(self) -> None:
        self._tsdb = self._fw.DB.active_tsdb
        self._graphdb = self._fw.DB.active_graphdb

    def ignore_failed_validation(self, ignore: bool) -> None:
        self._ignores_failed_validation = ignore

    def _create_output(self, data: Any, data_type:DatasetType|None) -> FetchOutput:
        if data_type is None:
            return FetchOutput(data, FetchStatus.OK)
        
        if not self._fw.Validator.validate(json.dumps(data), data_type):
            if self._ignores_failed_validation:
                return FetchOutput(data, FetchStatus.WARNING)
            return FetchOutput(None, FetchStatus.FAILED)
            
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

            if node['object_type'] == 'SOIL_SENSOR_READING':
                reading = SensorReading(json.dumps(node['data']))
                node['data']['values'] = self._tsdb.get_measurement_data(reading)

            data.append(node)

        
        return self._create_output(data, DatasetType.DATAMODEL)

    def steps(self, index:int=-1) -> FetchOutput:
        self._get_current_dbs()

        data=[]
        for node in self._graphdb.macht_label('MMPD_PROCESSSTEP'):
            if node is None:
                continue

            step_data = json.loads(str(node.get('data')))

            if (step_data['attributes']['index']['value'] != index) and (index != -1):
                continue

            data.append(step_data)

            for ref in step_data['references'].keys():
                if (ref == 'NEXT') or (ref == 'PREVIOUS'): continue

                for ref_node in self._graphdb.run('MATCH (a {id: $uuid})-[:' + ref + ']->(b) RETURN b', uuid=step_data['uuid']):
                    if ref_node['b'] is None: continue
                    ref_data = ref_node['b'].get('data')
                    assert(isinstance(ref_data, str))
                    data.append(json.loads(ref_data))

            if index != -1:
                break

        return self._create_output(data, DatasetType.DATAMODEL)

    def sensor_mea(self, id:str='') -> FetchOutput:
        ...

    # TODO: Step, shopflor, mea selection
    def components(self, id:str='', step:str='', shopfloor:str='', include_mea:bool=False) -> FetchOutput:
        self._get_current_dbs()
        data = []

        for node in self._graphdb.macht_label('SOIL_COMPONENT'):
            if node is None: continue
            node_data = json.loads(str(node.get('data')))
            if len(id) > 0 and node_data['uuid'] != id:
                continue

            data.append(node_data)

        return self._create_output(data, DatasetType.DATAMODEL)

    # TODO: Step selection
    def products(self, step:int=-1, include_specification:bool=False) -> FetchOutput:
        self._get_current_dbs()

        data=[]
        for node in self._graphdb.macht_label('MMPD_PRODUCT'):
            if node is None:
                continue
            
            node = json.loads(str(node.get('data')))
            data.append(node)
            
            if include_specification:
                for product in self._graphdb.run('MATCH (a)-[:PRODUCT_SPECIFICATION]->(b) RETURN b', uuid=node['uuid']):
                    if product['b'] is None: continue
                    prod = product['b'].get('data')
                    assert(isinstance(prod, str))
                    data.append(json.loads(prod))

        return self._create_output(data, DatasetType.DATAMODEL)

    def batches(self, include_products:bool=True) -> FetchOutput:
        self._get_current_dbs()

        data = []
        for node in self._graphdb.macht_label('MMPD_BATCH'):
            if node is None:
                continue

            node = dict(node)['data']
            node = json.loads(str(node))
            data.append(node)

            if include_products:
                for product in self._graphdb.run('MATCH (a {id: $uuid})-[:PRODUCTS]->(b) RETURN b', uuid=node['uuid']):
                    if product['b'] is None: continue
                    prod = product['b'].get('data')
                    assert(isinstance(prod, str))
                    data.append(json.loads(prod))
        
        return self._create_output(data, DatasetType.DATAMODEL)

    def invalid_datasets(self, ignore_model_data:bool=False, ignore_sensor_data:bool=False, limit:int=-1) -> FetchOutput:
        self._get_current_dbs()
        data = []

        for node in self._graphdb.macht_label('INVALID', limit):
            if node is None: continue

            node_data = json.loads(str(node.get('data')))

            if (node.get('type') == 'SOIL_DATA') and not ignore_sensor_data:
                data.append(node_data)

            if (node.get('type') == 'DATAMODEL') and not ignore_model_data:
                data.append(node_data)

        return self._create_output(data, None)
    
    def virtual_sensors(self, sensor:str='', step:str='') -> FetchOutput:
        ...