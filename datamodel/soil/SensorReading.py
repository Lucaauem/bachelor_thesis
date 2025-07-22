from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import json

if TYPE_CHECKING:
    from datamodel.Model import Model
    from datamodel.soil.Component import Component

class SensorReading:
    _data: dict
    _mea_id: str
    _model: Optional[Model] = None
    _sensor: Component

    def __init__(self, json_string: str) -> None:
        data = json.loads(json_string)
        uuid = data['uuid']
        timestamp = data['timestamp']

        self._data = data
        self._mea_id = f'{uuid}@{timestamp}'

    def serialize(self) -> dict:
        tmp_data = {
            'uuid': self._data['uuid'],
            'mea_id': self._mea_id,
            'data': self._data.copy(),
            'object_type' : 'SOIL:SENSOR_READING',
            'sensor': self._sensor.uuid
        }

        return tmp_data
    
    @property
    def timestamp(self) -> str:
        return self._data['timestamp']

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
    
    @property
    def model(self) -> Model | None:
        return self._model
    
    @model.setter
    def model(self, model: Model) -> None:
        self._model = model

    @property
    def sensor(self) -> Component:
        return self._sensor
    
    @sensor.setter
    def sensor(self, sensor: Component) -> None:
        assert sensor.is_sensor()

        self._sensor = sensor