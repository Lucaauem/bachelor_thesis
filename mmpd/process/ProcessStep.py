from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.process.Operator import Operator
    from mmpd.process.ProcessFlow import ProcessFlow
    from mmpd.product.PreProduct import PreProduct
    from mmpd.product.Product import Product
    from mmpd.process.ProcessStepSpecification import ProcessStepSpecification
    from soil.Sensor import Sensor
    from soil.SensorReading import SensorReading
    from mmpd.resource.Machine import Machine

class ProcessStep:
    __index: int
    __process_flow: ProcessFlow
    __operator: Operator
    __process_step_specification: ProcessStepSpecification
    __pre_product: PreProduct
    __product: Product
    __next: ProcessStep
    __tool: Sensor
    __sensor_readings: set[SensorReading]
    __machine: Machine

    def __init__(self, process: ProcessFlow, index: int) -> None:
        self.__index = index
        self.__process_flow = process
        self.__sensor_readings = set()

    def add_sensor_reading(self, reading: SensorReading) -> None:
        self.__sensor_readings.add(reading)

    @property
    def index(self) -> int:
        return self.__index

    @property
    def operator(self) -> Operator:
        return self.__operator
    
    @property
    def pre_product(self) -> PreProduct:
        return self.__pre_product
    
    @property
    def process_flow(self) -> ProcessFlow:
        return self.__process_flow
    
    @property
    def product(self) -> Product:
        return self.__product
    
    @property
    def next(self) -> ProcessStep:
        return self.__next
    
    @property
    def machine(self) -> Machine:
        return self.__machine
    
    @machine.setter
    def machine(self, machine: Machine) -> None:
        self.__machine = machine
    
    @property
    def tool(self) -> Sensor:
        return self.__tool
    
    @property
    def all_readings(self) -> set[SensorReading]:
        return self.__sensor_readings
    
    @tool.setter
    def tool(self, tool: Sensor) -> None:
        assert tool.is_tool()
        self.__tool = tool

    @next.setter
    def next(self, next: ProcessStep) -> None:
        self.__next = next
    
    @operator.setter
    def operator(self, operator: Operator) -> None:
        self.__operator = operator
        operator.add_to_step(self)

    @pre_product.setter
    def pre_product(self, pre_product: PreProduct) -> None:
        self.__pre_product = pre_product
        pre_product.add_to_step(self)

    @product.setter
    def product(self, product: Product) -> None:
        self.__product = product
        product.add_to_step(self)

    @property
    def specification(self) -> ProcessStepSpecification:
        return self.__process_step_specification
    
    @specification.setter
    def specification(self, specification: ProcessStepSpecification) -> None:
        self.__process_step_specification = specification