from __future__ import annotations
from typing import TYPE_CHECKING
from database.validation.rules.CorrectFormat import CorrectFormat

if TYPE_CHECKING:
    from database.validation.ValidationRule import ValidationRule
    from database.DatasetType import DatasetType

class Validator:
    _rules: set[ValidationRule]

    def __init__(self) -> None:
        basic_rules = []
        basic_rules.append(CorrectFormat())

        self._rules = set(basic_rules)

    def validate(self, data: str, type: DatasetType) -> bool:
        return all(rule.validate(data, type) for rule in self._rules)
