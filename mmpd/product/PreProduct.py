from __future__ import annotations
from typing import TYPE_CHECKING
from mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep
    from mmpd.product.ProductSpecification import ProductSpecification

class PreProduct(ProductionObject):
    __specification: ProductSpecification
    __process_steps: set[ProcessStep]

    def __init__(self, uuid: str) -> None:
        super().__init__(uuid)
        self.__process_steps = set()

    def add_to_step(self, step: ProcessStep) -> None:
        self.__process_steps.add(step)

    @property
    def specification(self) -> ProductSpecification:
        return self.__specification
    
    @specification.setter
    def specification(self, specification: ProductSpecification) -> None:
        self.__specification = specification
