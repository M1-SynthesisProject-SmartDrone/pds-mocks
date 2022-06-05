from enum import Enum, auto

class MediatorMode(Enum):
    IDLE = auto(),
    RECORD = auto(),
    AUTOPILOT = auto(),
    ERROR = auto()