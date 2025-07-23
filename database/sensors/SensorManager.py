import json

class SensorManager:
    def add_sensor(self, sensor: str) -> None:
        #print(sensor)
        ...

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