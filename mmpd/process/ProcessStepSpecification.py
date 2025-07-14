from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep

class ProcessStepSpecification:
    def __init__(self) -> None:
        self.__process_steps: set[ProcessStep] = set()


    def add_to_step(self, step: ProcessStep) -> None:
        if step in self.__process_steps:
            raise ValueError('Product already in this step')
        
        self.__process_steps.add(step)
        step.specification = self