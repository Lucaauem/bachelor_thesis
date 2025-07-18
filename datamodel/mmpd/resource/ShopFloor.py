from __future__ import annotations
from typing import TYPE_CHECKING
from datamodel.mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from datamodel.mmpd.resource.Machine import Machine
    from datamodel.soil.Component import Component
    from datamodel.Model import Model

class ShopFloor(ProductionObject):
    _REF_MACHINES = 'MACHINES'
    _REF_SENSORS = 'SENSORS'

    def __init__(self, uuid: str, model: Model) -> None:
        super().__init__(uuid, model)

    def add_machine(self, machine: Machine) -> None:
        self._add_reference(self._REF_MACHINES, machine)

    def add_sensor(self, Component: Component) -> None:
        assert not Component.is_tool()
        self._add_reference( self._REF_SENSORS, Component)
