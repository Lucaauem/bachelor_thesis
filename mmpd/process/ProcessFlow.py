from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep

class ProcessFlow(ProductionObject):
    __next: Optional[ProcessStep] = None
    __previous: Optional[ProcessStep] = None

    def __init__(self) -> None:
        super().__init__()

    @property
    def next(self) -> ProcessStep | None:
        return self.__next
    
    @next.setter
    def next(self, step: ProcessStep) -> None:
        self.__next = step

    @property
    def previous(self) -> ProcessStep | None:
        return self.__previous
    
    @previous.setter
    def previous(self, step: ProcessStep) -> None:
        self.__previous = step