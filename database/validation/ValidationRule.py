from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from database.DatasetType import DatasetType

class ValidationRule(ABC):
    @abstractmethod
    def validate(self, content: str, type: DatasetType) -> bool:
        pass