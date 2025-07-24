from enum import Enum, auto

class Events(Enum):
    STARTUP = auto(),
    SHUTDOWN = auto(),
    NEW_SENSOR_READING = auto(),
    MODEL_UPDATE = auto(),
    INVALID_DATASET = auto()