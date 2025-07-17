from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.ProductionObject import ProductionObject

class Model:
    __objects: set[ProductionObject]

    def __init__(self):
        self.__init__ = []

    def serialize(self) -> list[dict]:
        ...

    def add(self, object: ProductionObject) -> None:
        self.__objects.add(object)

    def get_object(self, uuid: str) -> ProductionObject | None:
        for obj in self.__objects:
            if obj.uuid == uuid:
                return obj
        return None