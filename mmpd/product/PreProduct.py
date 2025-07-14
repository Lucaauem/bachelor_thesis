from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep
    from mmpd.product.ProductSpecification import ProductSpecification

class PreProduct:
    __specifications: set[ProductSpecification]
    __process_steps: set[ProcessStep]

    def __init__(self) -> None:
        self.__specifications = set()

    def add_to_step(self, step: ProcessStep) -> None:
        if step in self.__process_steps:
            raise ValueError('PreProduct already in this step')
        
        self.__process_steps.add(step)

    @property
    def specifications(self) -> set[ProductSpecification]:
        return self.__specifications
    
    def add_specification(self, specification: ProductSpecification) -> None:
        self.__specifications.add(specification)
    