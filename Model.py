from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.ProductionObject import ProductionObject
    from soil.Sensor import Sensor
    from soil.SensorReading import SensorReading

class Model:
    _objects: set[ProductionObject | Sensor | SensorReading]

    def __init__(self):
        self._objects = set()

    def serialize(self) -> list:
        return [obj.serialize() for obj in self._objects]

    def add(self, object: ProductionObject | Sensor | SensorReading) -> None:
        self._objects.add(object)

    def get_object(self, uuid: str) -> ProductionObject | Sensor | SensorReading | None:
        for obj in self._objects:
            if obj.uuid == uuid:
                return obj
        return None
    
    @property
    def objects(self) -> set[ProductionObject | Sensor | SensorReading]:
        return self._objects
