from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep

class Operator:
    __process_steps: set[ProcessStep]

    def add_to_step(self, step: ProcessStep) -> None:
        if step in self.__process_steps:
            raise ValueError('Operator already in this step')
        
        self.__process_steps.add(step)
