from enum import Enum, auto

class State(Enum):
    RECEIVED = auto()
    VALIDATED = auto()
    SENT = auto()
    ACKED = auto()
    VISIBLE = auto()
    FAILED_RETRYABLE = auto()
    FAILED_NON_RETRYABLE = auto()
    SKIPPED = auto()