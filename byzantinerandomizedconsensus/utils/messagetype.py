from enum import Enum


class MessageType(Enum):
    NONE = -1
    PHASE1 = 1
    PHASE2 = 2
    SEND = 3
    ECHO = 4
    READY = 5