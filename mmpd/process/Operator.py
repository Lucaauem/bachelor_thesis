from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mmpd.process.ProcessStep import ProcessStep

class Operator:
    __process_steps: set[ProcessStep]

    def __init__(self) -> None:
        self.__process_steps = set()

    def add_to_step(self, step: ProcessStep) -> None:
        self.__process_steps.add(step)
