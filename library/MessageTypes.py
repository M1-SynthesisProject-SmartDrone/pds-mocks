"""Contains all message types along with their related string
"""

from enum import Enum
from typing import Optional

class MessageTypes(str, Enum):
    REQ_ACK = "ACK"
    REQ_START_DRONE = "START_DRONE"
    REQ_RECORD = "RECORD"
    REQ_MANUAL_CONTROL = "MANUAL_CONTROL"
    REQ_DRONE_INFOS = "DRONE_INFOS"
    REQ_PATH_LIST = "PATH_LIST"
    REQ_PATH_ONE = "PATH_ONE"
    REQ_PATH_LAUNCH = "PATH_LAUNCH"
    REQ_AUTOPILOT_INFOS = "AUTOPILOT_INFOS"
    REQ_REGAIN_CONTROL = "REGAIN_CONTROL"
    REQ_RESUME_AUTOPILOT = "RESUME_AUTOPILOT"
    
    RESP_ACK = "RESP_ACK"
    RESP_START_DRONE = "RESP_START_DRONE"
    RESP_RECORD = "RESP_RECORD"
    RESP_DRONE_INFOS = "RESP_DRONE_INFOS"
    RESP_PATH_LIST = "RESP_PATH_GET"
    RESP_PATH_ONE = "RESP_PATH_ONE"
    RESP_PATH_LAUNCH = "RESP_PATH_LAUNCH"
    RESP_AUTOPILOT_INFOS = "RESP_AUTOPILOT_INFOS"
    RESP_REGAIN_CONTROL = "RESP_REGAIN_CONTROL"
    RESP_RESUME_AUTOPILOT = "RESP_RESUME_AUTOPILOT"

    @staticmethod
    def find_from_value(value: str) -> "MessageTypes":
        msg_type = next((m for m in MessageTypes if m.value == value), None)
        if msg_type is None:
            raise ValueError(f"Cannot find {value} in the MessageTypes")
        return msg_type