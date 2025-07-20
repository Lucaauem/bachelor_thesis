from database.validation.ValidationRule import ValidationRule
from database.DatasetType import DatasetType
import json

class CorrectFormat(ValidationRule):
    def validate(self, content: str, type: DatasetType) -> bool:
        try:
            obj = json.loads(content)

            if (type == DatasetType.DATAMODEL) and (isinstance(obj, list)):
                return all(isinstance(sub, dict) for sub in obj)
            if (type == DatasetType.SOIL_DATA) and (isinstance(obj, dict)):
                return True
            return False
        except (ValueError, TypeError):
            return False
