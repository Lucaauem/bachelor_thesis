from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.resource.Machine import Machine
    from soil.Sensor import Sensor

class ShopFloor:
    __machines: set[Machine]
    __sensors: set[Sensor]

    def __init__(self) -> None:
        self.__machines = set()
        self.__sensors = set()

    def add_machine(self, machine: Machine) -> None:
        self.__machines.add(machine)

    def add_sensor(self, sensor: Sensor) -> None:
        assert not sensor.is_tool()
        self.__sensors.add(sensor)