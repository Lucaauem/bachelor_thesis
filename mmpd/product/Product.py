from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep
    from mmpd.product.Batch import Batch

class Product:

    def __init__(self) -> None:
        self.__process_step: Optional[ProcessStep] = None
        self.__batch: Optional[Batch] = None

    @property
    def process_step(self) -> ProcessStep | None:
        return self.__process_step
    
    @process_step.setter
    def process_step(self, step: ProcessStep) -> None:
        self.__process_step = step

    @property
    def batch(self) -> Batch | None:
        return self.__batch
    
    @batch.setter
    def batch(self, batch: Batch) -> None:
        self.__batch = batch