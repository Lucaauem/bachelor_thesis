from __future__ import annotations
from typing import TYPE_CHECKING
from soil.SensorType import SensorType

if TYPE_CHECKING:
    from soil.SensorReading import SensorReading

class Sensor:
    _uuid: str
    __type: SensorType
    __readings: set[SensorReading]
    ...

    def __init__(self, json_string: str, type: SensorType) -> None:
        self.__type = type
        self.__readings = set()
        self._uuid = ''

        ...

    def is_tool(self) -> bool:
        return self.__type == SensorType.TOOL
    
    def add_reading(self, reading: SensorReading) -> None:
        self.__readings.add(reading)

    @property
    def uuid(self) -> str:
        return self._uuid