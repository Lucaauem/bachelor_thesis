from typing import Union, Any

ALLOWED_TYPES = Union[str, int, float]

class ProductionObject:
    __attributes: dict[str, Any]
    
    def __init__(self) -> None:
        self.__attributes = {}

    def add_attribute(self, key: str, value: ALLOWED_TYPES) -> None:
        if not isinstance(value, (str, int, float)):
            raise TypeError(f"Value {value!r} must be str, int, or float")

        self.__attributes[key] = value

    @property
    def attributes(self) -> dict[str, Any]:
        return self.__attributes