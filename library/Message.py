
from dataclasses import dataclass, field
from typing import Any, Dict

import json

@dataclass
class Message:
    type: str
    content: Dict[str, Any]

    @classmethod
    def fromStr(cls, string: str) -> "Message":
        d = json.loads(string)
        return cls(d["type"], d["content"])

    def toJsonStr(self) -> str:
        d = {
            "type": self.type,
            "content": self.content
        }
        return json.dumps(d)