from enum import Enum, auto

class EventType(Enum):
    CREATE = auto()
    UPDATE = auto()
    DISABLE = auto()