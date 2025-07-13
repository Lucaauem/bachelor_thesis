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
    