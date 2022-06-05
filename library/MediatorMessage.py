
from dataclasses import dataclass, field
from typing import Any, Dict
from library.MediatorMessageTypes import MediatorMessageTypes

import json

from library.TcpSocket import TcpSocket

VALIDATED_KEY = "validated"

@dataclass
class MediatorMessage:
    type: MediatorMessageTypes
    content: Dict[str, Any]

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
