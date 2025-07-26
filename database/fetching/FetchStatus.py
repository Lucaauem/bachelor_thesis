from enum import Enum, auto

class FetchStatus(Enum):
    OK = auto()
    WARNING = auto()
    FAILED = auto()