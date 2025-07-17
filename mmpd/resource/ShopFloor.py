from __future__ import annotations
from typing import TYPE_CHECKING
from mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from mmpd.resource.Machine import Machine
    from soil.Sensor import Sensor
    from Model import Model

class ShopFloor(ProductionObject):
    REF_MACHINES = 'MACHINES'
    REF_SENSORS = 'SENSORS'

    def __init__(self, uuid: str, model: Model) -> None:
        super().__init__(uuid, model)

    def add_machine(self, machine: Machine) -> None:
        self._add_reference(self.REF_MACHINES, machine)

    def add_sensor(self, sensor: Sensor) -> None:
        assert not sensor.is_tool()
        self._add_reference( self.REF_SENSORS, sensor)
