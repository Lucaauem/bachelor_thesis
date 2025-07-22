from __future__ import annotations
from typing import TYPE_CHECKING, cast
from datamodel.mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from datamodel.mmpd.process.ProcessStep import ProcessStep
    from datamodel.mmpd.product.ProductSpecification import ProductSpecification
    from datamodel.Model import Model

class PreProduct(ProductionObject):
    _REF_STEPS = 'PRODUCT_STEPS'
    _REF_SPECIFICATION = 'PRODUCT_SPECIFICATION'

    _uuid_steps: list[str]
    _uuid_specification = ''

    def __init__(self, uuid: str, model: Model) -> None:
        super().__init__(uuid, model)
        self._uuid_steps = []

    @property
    def steps(self) -> list[ProcessStep | None]:
        return [cast(ProcessStep | None, self._model.get_object(step)) for step in self._uuid_steps]
    def add_to_step(self, step: ProcessStep) -> None:
        self._uuid_steps.append(step.uuid)
        self._add_reference(self._REF_STEPS, step)

    @property
    def specification(self) -> ProductSpecification | None:
        return cast(ProductSpecification | None, self._model.get_object(self._uuid_specification))
    @specification.setter
    def specification(self, specification: ProductSpecification) -> None:
        self._uuid_specification = specification.uuid
        self._add_reference(self._REF_SPECIFICATION, specification)
        specification.add_to_pre_product(self)
