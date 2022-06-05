"""Contains all message types along with their related string
"""

from enum import Enum

class MediatorMessageTypes(str, Enum):
    REQ_TR_SAVE = "TR_SAVE"
    REQ_TR_REGISTER = "REGISTER"
    REQ_TR_END_SAVE = "TR_END_SAVE"
    REQ_TR_LAUNCH = "TR_LAUNCH"
    REQ_TR_POINTS = "REQ_TR_POINTS"
    REQ_WAIT_TR_FILE = "WAIT_TR_FILE"
    REQ_RESP_TR_FILE = "RESP_TR_FILE"
    REQ_NEXTDRONEPOSITION = "NEXTDRONEPOSITION"
    REQ_RESP_DRONEPOSITION = "RESP_DRONEPOSITION"
    REQ_TR_ERROR = "TR_ERROR"
    REQ_END_TR_ERROR = "END_TR_ERROR"
    REQ_GET_PATH_LIST = "GET_PATH_LIST"
    REQ_GET_ONE_PATH = "GET_ONE_PATH"
    
    RESP_ACK = "ACK"
    RESP_TR_SAVE = "RESP_TR_SAVE"
    RESP_TR_REGISTER = "RESP_REGISTER"
    RESP_END_TR_SAVE = "RESP_END_TR_SAVE"
    RESP_TR_LAUNCH = "RESP_TR_LAUNCH"
    RESP_REQ_TR_POINTS = "RESP_REQ_TRIP_POINTS"
    RESP_TR_FILE = "TR_FILE"
    RESP_DRONEPOSITION = "DRONEPOSITION"
    RESP_ERROR = "ERROR_NOTIFICATION_RECEIVED"
    RESP_PATH_LIST = "RESP_PATH_LIST"
    RESP_ONE_PATH = "RESP_ONE_PATH"

    @staticmethod
    def find_from_value(value: str) -> "MediatorMessageTypes":
        msg_type = next((m for m in MediatorMessageTypes if m.value == value), None)
        if msg_type is None:
            raise ValueError(f"Cannot find {value} in the MediatorMessageTypes")
        return msg_type