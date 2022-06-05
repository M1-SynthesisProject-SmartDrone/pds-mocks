
import threading

from pathlib import Path
import sys
from typing import Callable, Dict

from mock_mediator_for_groundstation.modes import MediatorMode
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
# Must be put after sys.path.append
from library import * # noqa

from library.TcpSocket import TcpSocket
from MediatorMockInfos import MediatorMockInfos

# ==== THREAD MAIN PORT ====
class Thread1 (threading.Thread):
    def __init__(self, port: int) -> None:
        threading.Thread.__init__(self)
        self.name = "main_port"
        self.port: int = port
        self.tcp = TcpSocket()
        self.infos = MediatorMockInfos()

        self.handler_by_request: Dict[MediatorMessageTypes, Callable[[self, MediatorMessage], None]] = {
            MediatorMessageTypes.REQ_TR_SAVE: self.handle_tr_save,
            MediatorMessageTypes.REQ_TR_REGISTER: self.handle_register,
            MediatorMessageTypes.REQ_TR_END_SAVE: self.handle_end_tr_save,
            MediatorMessageTypes.REQ_TR_LAUNCH: self.handle_tr_launch,
            MediatorMessageTypes.REQ_TR_ERROR: self.handle_tr_error,
            MediatorMessageTypes.REQ_END_TR_ERROR: self.handle_tr_end_error,
            MediatorMessageTypes.REQ_GET_PATH_LIST: self.handle_get_path_list,
            MediatorMessageTypes.REQ_GET_ONE_PATH: self.handle_get_one_path,
        }
    
    def run(self) -> None:
        self.tcp.wait_connection(self.port)
        while self.infos.is_running:
            try:
                message = MediatorMessage.receive(self.tcp, True)
                handler = self.handler_by_request[message.type]
                handler(message)
            except Exception as err:
                logger.error(err)

    def handle_tr_save(self, msg: MediatorMessage):
        resp = MediatorMessage(MediatorMessageTypes.RESP_TR_SAVE.value, {"isLaunched": True})
        if self.infos.mode != MediatorMode.IDLE:
            logger.warning("Try to launch the save but not in idle mode")
            resp.content["isLaunched"] = False
        else:
            logger.info("Start record")
            self.infos.mode = MediatorMode.RECORD
        self.tcp.send(resp)
    
    def handle_register(self, msg: MediatorMessage):
        resp_name = MediatorMessageTypes.RESP_TR_REGISTER.value
        imageSize: int = msg.content["imageSize"]
        # Multiple requests possible
        if self.infos.mode == MediatorMode.IDLE:
            logger.warning("Try to register but in idle mode")
            resp = MediatorMessage(resp_name, {"isDone": False})
            self.tcp.send(resp.toJsonStr())
        else:
            mode_name = self.infos.mode.name
            logger.info(f"\"Register\" a point in mode {mode_name} : {msg.content}")
            resp = MediatorMessage(resp_name, {"isDone": True})
            self.tcp.send(resp.toJsonStr())
            # Receive the image
            self.infos.last_image_received = self.tcp.receive_bytes(imageSize)
            logger.info("Image received !")


    def handle_end_tr_save(self, msg: MediatorMessage):
        resp = MediatorMessage(MediatorMessageTypes.RESP_END_TR_SAVE.value, {"isDone": True})
        if self.infos.mode != MediatorMode.RECORD:
            logger.warning("Try to launch the save but not in record mode")
            resp.content["isDone"] = False
        else:
            logger.info("End record")
            self.infos.mode = MediatorMode.IDLE
        self.tcp.send(resp)

    def handle_tr_launch(self, msg: MediatorMessage):
        resp = MediatorMessage(MediatorMessageTypes.RESP_TR_LAUNCH.value, {"isDone": True})
        id: int = msg.content["tr_id"]
        if self.infos.mode != MediatorMode.IDLE:
            logger.warning("Try to launch a trip but not in idle mode")
            resp.content["isDone"] = False
        else:
            logger.info(f"Start trip n°{id}")
            self.infos.mode = MediatorMode.AUTOPILOT
        self.tcp.send(resp)

    def handle_tr_error(self, msg: MediatorMessage):
        resp = MediatorMessage(MediatorMessageTypes.RESP_ERROR.value, {})
        if self.infos.mode != MediatorMode.AUTOPILOT:
            logger.warning("Try to go in error mode but was not in autopilot mode")
        else:
            logger.info(f"Start error mode")
            self.infos.mode = MediatorMode.ERROR
        self.tcp.send(resp)

    def handle_tr_end_error(self, msg: MediatorMessage):
        resp = MediatorMessage(MediatorMessageTypes.RESP_ERROR.value, {})
        if self.infos.mode != MediatorMode.ERROR:
            logger.warning("Try to stop error mode but was not in error mode")
        else:
            logger.info(f"Stop error mode")
            self.infos.mode = MediatorMode.AUTOPILOT
        self.tcp.send(resp)

    def handle_get_path_list(self, msg: MediatorMessage):
        pass

    def handle_get_one_path(self, msg: MediatorMessage):
        pass
