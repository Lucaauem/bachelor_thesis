from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep
    from mmpd.product.ProductSpecification import ProductSpecification

class PreProduct:
    __specification: ProductSpecification
    __process_steps: set[ProcessStep]

    def add_to_step(self, step: ProcessStep) -> None:
        if step in self.__process_steps:
            raise ValueError('PreProduct already in this step')
        
        self.__process_steps.add(step)

    @property
    def specification(self) -> ProductSpecification:
        return self.__specification
    
    @specification.setter
    def specification(self, specification: ProductSpecification) -> None:
        self.__specification = specification
