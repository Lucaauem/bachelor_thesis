from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datamodel.mmpd.ProductionObject import ProductionObject
    from datamodel.soil.Component import Component
    from datamodel.soil.SensorReading import SensorReading

class Model:
    _objects: set[ProductionObject | Component | SensorReading]

    def __init__(self):
        self._objects = set()

    def serialize(self) -> list:
        return [obj.serialize() for obj in self._objects]

    def add(self, object: ProductionObject | Component | SensorReading) -> None:
        self._objects.add(object)

    def get_object(self, uuid: str) -> ProductionObject | Component | SensorReading | None:
        for obj in self._objects:
            if obj.uuid == uuid:
                return obj
        return None
    
    @property
    def objects(self) -> set[ProductionObject | Component | SensorReading]:
        return self._objects
