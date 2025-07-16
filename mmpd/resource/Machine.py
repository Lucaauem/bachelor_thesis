from __future__ import annotations
from typing import TYPE_CHECKING
from mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from soil.Sensor import Sensor

class Machine(ProductionObject):
    __tools : set[Sensor]
    __sensors: set[Sensor]

    def __init__(self) -> None:
        super().__init__()
        self.__tools = set()
        self.__sensors = set()

    def add_tool(self, tool: Sensor) -> None:
        assert tool.is_tool()
        self.__tools.add(tool)

    def add_sensor(self, sensor: Sensor) -> None:
        assert not sensor.is_tool()
        self.__sensors.add(sensor)