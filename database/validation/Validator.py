from __future__ import annotations
from typing import TYPE_CHECKING
from database.validation.rules.CorrectFormat import CorrectFormat
from database.callbacks.Events import Events as CallbackEvents

from database.DatasetType import DatasetType
if TYPE_CHECKING:
    from database.validation.ValidationRule import ValidationRule
    from database.DBFramework import DBFramework

class Validator:
    _rules: set[ValidationRule]
    _fw: DBFramework

    def __init__(self, fw_instance: DBFramework) -> None:
        basic_rules = []
        basic_rules.append(CorrectFormat())

        self._rules = set(basic_rules)
        self._fw = fw_instance

    def add_rule(self, rule: ValidationRule) -> None:
        self._rules.add(rule)

    def validate(self, data: str, type: DatasetType) -> bool:
        status = all(rule.validate(data, type) for rule in self._rules)

        if not status:
            self._fw.Callbacks.trigger(CallbackEvents.INVALID_DATASET, data=data)
            
        return status
