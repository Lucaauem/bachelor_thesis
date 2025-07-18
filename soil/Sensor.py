from __future__ import annotations
from typing import TYPE_CHECKING, override
from soil.SensorType import SensorType
import json

if TYPE_CHECKING:
    from soil.SensorReading import SensorReading
    from Model import Model

class Sensor:
    _type: SensorType
    _readings: set[SensorReading]
    _data: dict
    _model: Model

    def serialize(self) -> dict:
        tmp_data = self._data.copy()
        tmp_data['references'] = { 'READINGS' : list() }

        for reading in self._readings:
            tmp_data['references']['READINGS'].append(reading.id)
        
        return tmp_data

    def __init__(self, json_string: str, type: SensorType, model: Model) -> None:
        self._data = json.loads(json_string)
        self._model = model
        self._type = type
        self._readings = set()
        model.add(self)

    def is_tool(self) -> bool:
        return self._type == SensorType.TOOL
    
    def is_sensor(self) -> bool:
        return self._type == SensorType.REAL or self._type == SensorType.VIRTUAL
    
    def add_reading(self, reading: SensorReading) -> None:
        self._readings.add(reading)
        reading.model = self._model
        self._model.add(reading)

    @property
    def uuid(self) -> str:
        return self._data['uuid']
    
    @property
    def type(self) -> SensorType:
        return self._type
