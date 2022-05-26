"""Contains all message types along with their related string
"""

from enum import Enum

class MediatorMessageTypes(str, Enum):
    REQ_TR_SAVE = "TR_SAVE"
    REQ_TR_REGISTER = "TR_REGISTER"
    REQ_TR_END_SAVE = "TR_END_SAVE"
    
    RESP_ACK = "ACK"
    RESP_TR_SAVE = "RESP_TR_SAVE"
    RESP_END_TR_SAVE = "RESP_END_TR_SAVE"

    @staticmethod
    def find_from_value(value: str) -> "MediatorMessageTypes":
        msg_type = next((m for m in MediatorMessageTypes if m.value == value), None)
        if msg_type is None:
            raise ValueError(f"Cannot find {value} in the MediatorMessageTypes")
        return msg_type