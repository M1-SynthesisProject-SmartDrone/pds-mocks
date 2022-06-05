
from dataclasses import dataclass, field
from typing import Any, Dict
from library.MediatorMessageTypes import MediatorMessageTypes

import json

from library.TcpSocket import TcpSocket

VALIDATED_KEY = "validated"

class MediatorMessage:
    def __init__(self, type: MediatorMessageTypes, content: Dict[str, Any], is_request: bool = True) -> None:
        self.type: MediatorMessageTypes = type
        self.content: Dict[str, Any] = content
        if is_request:
            self.content["requestType"] = type.value
        else:
            self.content["responseType"] = type.value

    @classmethod
    def fromStr(cls, string: str, is_request: bool = True) -> "MediatorMessage":
        d = json.loads(string)
        if is_request:
            return cls(MediatorMessageTypes.find_from_value(d["requestType"]), d)
        else:
            return cls(MediatorMessageTypes.find_from_value(d["responseType"]), d)

    @classmethod
    def receive(cls, socket: TcpSocket, is_request: bool = True) -> "MediatorMessage":
        return MediatorMessage.fromStr(socket.receive(), is_request)

    def toJsonStr(self) -> str:
        return json.dumps(self.content)
