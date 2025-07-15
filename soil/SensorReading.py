import json
from typing import Optional

class SensorReading:
    __uuid: str
    __name: str
    __description: str
    __datatype: str
    __value: list
    __dimension: list
    __range: list
    __timestamp: str
    __label: Optional[str] = None
    __covariance: list
    __unit: str
    __mea_id: str

    def __init__(self, json_string: str) -> None:
        data: dict = json.loads(json_string)

        for key, value in data.items():
            mangled_name = f"_{self.__class__.__name__}__{key}"
            setattr(self, mangled_name, value)

        self.__mea_id = f'{self.__uuid}@{self.__timestamp}'

    @property
    def uuid(self) -> str:
        return self.__uuid
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> str:
        return self.__mea_id
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def data_type(self) -> str:
        return self.__datatype
    
    @property
    def value(self) -> list:
        return self.__value
    
    @property
    def dimension(self) -> list:
        return self.__dimension
    
    @property
    def range(self) -> list:
        return self.__range
    
    @property
    def label(self) -> str | None:
        return self.__label
    
    @property
    def covariance(self) -> list:
        return self.__covariance
    
    @property
    def unit(self) -> str:
        return self.__unit