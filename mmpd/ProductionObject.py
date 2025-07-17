from typing import Union, Any

ALLOWED_TYPES = Union[str, int, float]

class ProductionObject:
    __UUID: str
    __attributes: dict[str, Any]
    __references: dict[str, Any]
    
    def __init__(self, uuid: str) -> None:
        self.__UUID = uuid
        self.__attributes = {}

    def add_attribute(self, key: str, value: ALLOWED_TYPES) -> None:
        if not isinstance(value, (str, int, float)):
            raise TypeError(f"Value {value!r} must be str, int, or float")

        self.__attributes[key] = value

    def set_attributes(self, **attributes) -> None:
        self.__attributes = attributes

    @property
    def attributes(self) -> dict[str, Any]:
        return self.__attributes
    
    @property
    def uuid(self) -> str:
        return self.__UUID