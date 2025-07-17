from __future__ import annotations
from typing import TYPE_CHECKING, Union, Any

if TYPE_CHECKING:
    from mmpd.ProductionObject import ProductionObject
    from Model import Model
    from soil.Sensor import Sensor
    from soil.SensorReading import SensorReading

ALLOWED_TYPES = Union[str, int, float]

class ProductionObject:
    __UUID: str
    __attributes: dict[str, Any]
    __references: dict[str, set[str]]
    _model: Model
    
    def __init__(self, uuid: str, model: Model) -> None:
        self.__UUID = uuid
        self.__attributes = {}
        self.__references = {}
        self._model = model
        model.add(self)

    def add_attribute(self, key: str, value: ALLOWED_TYPES) -> None:
        if not isinstance(value, (str, int, float)):
            raise TypeError(f"Value {value!r} must be str, int, or float")

        self.__attributes[key] = value

    def set_attributes(self, **attributes) -> None:
        self.__attributes = attributes

    def _add_reference(self, type: str, object: ProductionObject | Sensor | SensorReading) -> None:
        if type not in self.__references.keys():
            self.__references[type] = set()

        self.__references[type].add(object.uuid)

    @property
    def attributes(self) -> dict[str, Any]:
        return self.__attributes
    
    @property
    def uuid(self) -> str:
        return self.__UUID
    
    @property
    def references(self) -> dict[str, set[str]]:
        return self.__references