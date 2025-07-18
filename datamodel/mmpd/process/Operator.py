from __future__ import annotations
from typing import TYPE_CHECKING
from datamodel.mmpd.ProductionObject import ProductionObject

if TYPE_CHECKING:
    from datamodel.mmpd.process.ProcessStep import ProcessStep
    from datamodel.Model import Model

class Operator(ProductionObject):
    _REF_STEPS = 'PROCESS_STEPS'

    def __init__(self, uuid: str, model: Model) -> None:
        super().__init__(uuid, model)

    def add_to_step(self, step: ProcessStep) -> None:
        self._add_reference(self._REF_STEPS, step)
