from __future__ import annotations
from typing import TYPE_CHECKING, cast
from datamodel.mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from datamodel.mmpd.process.Operator import Operator
    from datamodel.mmpd.product.PreProduct import PreProduct
    from datamodel.mmpd.product.Product import Product
    from datamodel.mmpd.process.ProcessStepSpecification import ProcessStepSpecification
    from datamodel.soil.Component import Component
    from datamodel.soil.SensorReading import SensorReading
    from datamodel.mmpd.resource.Machine import Machine
    from datamodel.Model import Model

class ProcessStep(ProductionObject):
    _REF_NEXT_STEP = 'NEXT'
    _REF_PREV_STEP = 'PREVIOUS'
    _REF_OPERATOR = 'OPERATOR'
    _REF_STEP_SPECIFICATION = 'PROCESS_STEP_SPECIFICATION'
    _REF_PRE_PRODUCT = 'PRE_PRODUCT'
    _REF_PRODUCT = 'PRODUCT'
    _REF_TOOL = 'TOOL'
    _REF_SENSOR_READINGS = 'SENSOR_READINGS'
    _REF_MACHINE = 'MACHINE'

    _uuid_next: str = ''
    _uuid_prev: str = ''
    _uuid_operator: str = ''
    _uuid_process_step_specification: str = ''
    _uuid_pre_product: str = ''
    _uuid_product: str = ''
    _uuid_tool: str = ''
    _uuid_sensor_readings: list[str]
    _uuid_machine: str = ''

    def __init__(self, uuid: str, model: Model) -> None:
        super().__init__(uuid, model)
        self._uuid_sensor_readings = []

    @property
    def next_step(self) -> ProcessStep | None:
        return cast(ProcessStep | None, self._model.get_object(self._uuid_next))
    @next_step.setter
    def next_step(self, next: ProcessStep) -> None:
        self._uuid_next = next.uuid
        self._add_reference(self._REF_NEXT_STEP, next)

    @property
    def previous_step(self) -> ProcessStep | None:
        return cast(ProcessStep | None, self._model.get_object(self._uuid_prev))
    @previous_step.setter
    def previous_step(self, previous: ProcessStep) -> None:
        self._uuid_next = previous.uuid
        self._add_reference(self._REF_PREV_STEP, previous)

    @property
    def operator(self) -> Operator | None:
        return cast(Operator | None, self._model.get_object(self._uuid_operator))
    @operator.setter
    def operator(self, operator: Operator) -> None:
        self._uuid_operator = operator.uuid
        self._add_reference(self._REF_OPERATOR, operator)
        operator.add_to_step(self)
        
    @property
    def specification(self) -> ProcessStepSpecification | None:
        return cast(ProcessStepSpecification | None, self._model.get_object(self._uuid_process_step_specification))
    @specification.setter
    def specification(self, process_step_specification: ProcessStepSpecification) -> None:
        self._uuid_process_step_specification = process_step_specification.uuid
        self._add_reference(self._REF_STEP_SPECIFICATION, process_step_specification)

    @property
    def pre_product(self) -> PreProduct | None:
        return cast(PreProduct | None, self._model.get_object(self._uuid_pre_product))
    @pre_product.setter
    def pre_product(self, pre_product: PreProduct) -> None:
        self._uuid_pre_product = pre_product.uuid
        self._add_reference(self._REF_PRE_PRODUCT, pre_product)

    @property
    def product(self) -> Product | None:
        return cast(Product | None, self._model.get_object(self._uuid_product))
    @product.setter
    def product(self, product: Product) -> None:
        self._uuid_product = product.uuid
        self._add_reference(self._REF_PRODUCT, product)

    @property
    def tool(self) -> Component | None:
        return cast(Component | None, self._model.get_object(self._uuid_tool))
    @tool.setter
    def tool(self, tool: Component) -> None:
        assert(tool.is_tool())
        self._uuid_tool = tool.uuid
        self._add_reference(self._REF_TOOL, tool)

    @property
    def sensor_readings(self) -> list[SensorReading | None]:
        return [cast(SensorReading | None, self._model.get_object(reading)) for reading in self._uuid_sensor_readings]
    def add_sensor_reading(self, reading: SensorReading) -> None:
        self._uuid_sensor_readings.append(reading.id) #TODO TO CORRECT ID
        self._add_reference(self._REF_SENSOR_READINGS, reading)

    @property
    def machine(self) -> Machine | None:
        return cast(Machine | None, self._model.get_object(self._uuid_machine))
    @machine.setter
    def machine(self, machine: Machine) -> None:
        self._uuid_machine = machine.uuid
        self._add_reference(self._REF_MACHINE, machine)
