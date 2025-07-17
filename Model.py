from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.ProductionObject import ProductionObject

class Model:
    _objects: set[ProductionObject]

    def __init__(self):
        self._objects = set()

    def serialize(self) -> list[dict]:
        ...

    def add(self, object: ProductionObject) -> None:
        self._objects.add(object)

    def get_object(self, uuid: str) -> ProductionObject | None:
        for obj in self._objects:
            if obj.uuid == uuid:
                return obj
        return None
    
    @property
    def objects(self) -> set[ProductionObject]:
        return self._objects
