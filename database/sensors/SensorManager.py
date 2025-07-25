from datamodel.soil.Component import Component
from datamodel.soil.ComponentType import ComponentType
from database.Log import log
import json

class SensorManager:
    _sensors: dict[str, Component]

    def __init__(self) -> None:
        self._sensors = {}

    def add_sensor(self, sensor: dict) -> None:
        component = Component(json.dumps(sensor), ComponentType.REAL, None)
        self._sensors[component.uuid] = component
        
        log(f'Sensors: Added "{component.uuid}"')

    def on_new_data(self, raw_data: str) -> tuple[str, dict] | None:
        data = self._parse_data(raw_data)

        if len(data) == 0:
            return
        
        if 'value' not in data.keys(): # Sensor description
            return
        
        sensor_uuid = data['uuid'].split('/')[0]
        return (sensor_uuid, data)

    def _parse_data(self, data: str) -> dict:
        try:
            json_data = json.loads(data)
            if isinstance(json_data, dict):
                return json_data
            return {}
        except: # No data
            return {}