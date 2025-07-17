from __future__ import annotations
from typing import TYPE_CHECKING
from mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from soil.Sensor import Sensor
    from Model import Model

class Machine(ProductionObject):
    _REF_TOOLS = 'TOOLS'
    _REF_SENSORS = 'SENSORS'

    def __init__(self, uuid: str, model: Model) -> None:
        super().__init__(uuid, model)

    def add_tool(self, tool: Sensor) -> None:
        assert tool.is_tool()
        self._add_reference(self._REF_TOOLS, tool)

    def add_sensor(self, sensor: Sensor) -> None:
        assert not sensor.is_tool()
        self._add_reference(self._REF_SENSORS, sensor)
