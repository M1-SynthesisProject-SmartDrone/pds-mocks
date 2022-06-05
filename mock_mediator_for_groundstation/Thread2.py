
import json
import threading

from pathlib import Path
import sys
from typing import Callable, Dict
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
# Must be put after sys.path.append
from library import * # noqa

from library.TcpSocket import TcpSocket
from MediatorMockInfos import MediatorMockInfos
from paths import PATH_LIST, PATH_ONE_LIST

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
                handler = self.handler_by_request[message.type]
                handler(self, message)
            except Exception as err:
                logger.error(err)

    def handle_req_tr_points(self, msg: MediatorMessage):
        logger.info("Get all checkpoints of trip")
        id = self.infos.current_tr_id
        r = MediatorMessage(MediatorMessageTypes.RESP_TR_FILE.value, {"content": PATH_ONE_LIST[id]})
        msg_bytes = r.toJsonStr().encode("utf-8")
        # intermediary message
        resp = MediatorMessage(MediatorMessageTypes.RESP_REQ_TR_POINTS.value, {"filesize": len(msg_bytes)})
        self.tcp.send(resp.toJsonStr())

        message = MediatorMessage.receive(self.tcp, True)
        if message.type != MediatorMessageTypes.REQ_WAIT_TR_FILE:
            logger.warning(f"Didn't receive wanted message type (got {message.type.value})")
        
        logger.info(f"Prepare to send {len(msg_bytes)} bytes of data")
        self.tcp.send_bytes(msg_bytes)

    def handle_nexdroneposition(self, msg: MediatorMessage):
        logger.info("Get new drone position")
        id = self.infos.current_tr_id
        resp = MediatorMessage(MediatorMessageTypes.RESP_DRONEPOSITION.value, {
            "id_pos": self.infos.current_checkpoint_index,
            "imageSize": len(self.infos.image)
        })
        self.tcp.send(resp.toJsonStr())
        self.infos.current_checkpoint_index += 1

        m = MediatorMessage.receive(self.tcp, True)
        self.tcp.send_bytes(self.infos.image)

