
import threading

from pathlib import Path
import sys
from typing import Callable, Dict
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
# Must be put after sys.path.append
from library import * # noqa

from library.TcpSocket import TcpSocket
from MediatorMockInfos import MediatorMockInfos

# ==== THREAD SECONDARY PORT ====
class Thread2 (threading.Thread):
    def __init__(self, port: int) -> None:
        threading.Thread.__init__(self)
        self.name = "secondary_port"
        self.port: int = port
        self.tcp = TcpSocket()
        self.infos = MediatorMockInfos()
    
        self.handler_by_request: Dict[MediatorMessageTypes, Callable[[self, MediatorMessage], None]] = {
            MediatorMessageTypes.REQ_TR_POINTS: self.handle_req_tr_points,
            MediatorMessageTypes.REQ_NEXTDRONEPOSITION: self.handle_nexdroneposition
        }
    
    def run(self) -> None:
        self.tcp.wait_connection(self.port)
        while self.infos.is_running:
            try:
                message = MediatorMessage.receive(self.tcp, True)
            except Exception as err:
                logger.error(err)

    def handle_req_tr_points(self, msg: MediatorMessage):
        # Multiple sub requests
        pass

    def handle_nexdroneposition(self, msg: MediatorMessage):
        # Multiple sub requests
        pass
