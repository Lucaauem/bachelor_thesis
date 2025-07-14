from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep
    from mmpd.product.Batch import Batch
    from mmpd.product.ProductSpecification import ProductSpecification

class Product:
    __specification: ProductSpecification
    __process_steps: set[ProcessStep]
    __batch: Optional[Batch]

    def __init__(self) -> None:
        self.__process_steps = set()
        self.__batch = None

    @property
    def process_step(self) -> set[ProcessStep]:
        return self.__process_steps
    
    def add_to_step(self, step: ProcessStep) -> None:
        if step in self.__process_steps:
            raise ValueError('Product already in this step')
        
        self.__process_steps.add(step)

    @property
    def batch(self) -> Batch | None:
        return self.__batch
    
    @batch.setter
    def batch(self, batch: Batch) -> None:
        self.__batch = batch

    @property
    def specification(self) -> ProductSpecification:
        return self.__specification
    
    @specification.setter
    def specification(self, specification: ProductSpecification) -> None:
        self.__specification = specification