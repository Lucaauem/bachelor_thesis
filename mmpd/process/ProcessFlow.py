from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep

class ProcessFlow():
    __name : str
    __steps : list[ProcessStep] # TODO Maybe swap to linked list

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__steps = []

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def next_step(self) -> ProcessStep:
        return self.__steps[0]
    
    def add_step(self) -> ProcessStep:
        from mmpd.process.ProcessStep import ProcessStep
        
        new_step = ProcessStep(self, len(self.__steps))

        if len(self.__steps) > 0:
            self.__steps[-1].next = new_step

        self.__steps.append(new_step)
        return new_step
    
    def step_next_step(self) -> ProcessStep:
        self.__steps.pop(0)
        return self.__steps[0]