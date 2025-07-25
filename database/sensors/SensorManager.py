from datamodel.soil.Component import Component
from datamodel.soil.ComponentType import ComponentType
from database.sensors.Sensor import Sensor
from database.db.DBManager import DBManager
from database.Log import log
import json

class SensorManager:
    _sensors: dict[str, Sensor]
    _db: DBManager

    def __init__(self, db_manager: DBManager) -> None:
        self._sensors = {}
        self._db = db_manager

    def add_sensor(self, sensor: dict) -> None:
        component = Component(json.dumps(sensor), ComponentType.REAL, None)
        self._sensors[component.uuid] = Sensor(component, self._db)
        
        log(f'Sensors: Added "{component.uuid}"')

    def get_sensor(self, uuid: str) -> Sensor:
        return self._sensors[uuid]
    
    def get_all_sensors(self) -> list[Sensor]:
        return list(self._sensors.values())
    
    def is_correct_reading(self, raw_data: str) -> tuple[bool, str, dict]:
        data = self._parse_data(raw_data)

        if len(data) == 0:
            return (False, '', {})

        if 'value' not in data.keys(): # Sensor description
            return (False, '', {})
        
        sensor_uuid = data['uuid'].split('/')[0] # TODO Split sensor components into multiple objects
        return (True, sensor_uuid, data)

    def _parse_data(self, data: str) -> dict:
        try:
            json_data = json.loads(data)
            if isinstance(json_data, dict):
                return json_data
            return {}
        except: # No data
            return {}