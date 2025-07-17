import json

class SensorReading:
    _data: dict
    _mea_id: str

    def __init__(self, json_string: str) -> None:
        self._data = json.loads(json_string)

        uuid = self._data['uuid']
        timestamp = self._data['timestamp']

        self._mea_id = f'{uuid}@{timestamp}'

    @property
    def data(self) -> dict:
        return self._data

    @property
    def uuid(self) -> str:
        return self._data['uuid']
    
    @property
    def name(self) -> str:
        return self._data['name']

    @property
    def id(self) -> str:
        return self._mea_id
    
    @property
    def description(self) -> str:
        return self._data['description']
    
    @property
    def data_type(self) -> str:
        return self._data['datatype']
    
    @property
    def value(self) -> list:
        return self._data['value']
    
    @property
    def dimension(self) -> list:
        return self._data['dimension']
    
    @property
    def range(self) -> list:
        return self._data['range']
    
    @property
    def label(self) -> str | None:
        return self._data['label']
    
    @property
    def covariance(self) -> list:
        return self._data['covariance']
    
    @property
    def unit(self) -> str:
        return self._data['unit']