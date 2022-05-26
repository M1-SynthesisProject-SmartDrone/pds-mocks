""" This script will permits to emulate the ground station behavior :
it will :
 - connect to the server
 - send a TR_SAVE request
 - after confirmation, send multiple TR_REGISTER requests (with images)
 - after a certain amount of time, send a TR_END_SAVE request
"""
from typing import Callable, Dict
from loguru import logger
from time import sleep, time
from random import randint, random
from pathlib import Path
import cv2

import sys
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
# Must be put after sys.path.append
from library import * # noqa

PORT = 7070
IP_ADDRESS = "127.0.0.1"
tcp = TcpSocket()

def create_msg(type: MediatorMessageTypes, content: dict) -> MediatorMessage:
    content["requestType"] = type.value
    return MediatorMessage(type, content)

def send_receive(socket: TcpSocket, 
    message: MediatorMessage, 
    wanted_return_type: MediatorMessageTypes) -> MediatorMessage:
    socket.send(message.toJsonStr())
    resp = MediatorMessage.receive(socket)
    if resp.type.value != wanted_return_type.value:
        raise ValueError(f"Wanted {wanted_return_type.value} but got {resp.type.value}")
    return resp

def register_message(img_size: int) -> MediatorMessage:
    return create_msg(MediatorMessageTypes.REQ_TR_REGISTER, {
        "altitude": randint(0, 100),
        "latitude": randint(123456789, 999999999),
        "latitude": randint(123456789, 999999999),
        "rotation": randint(0, 65355),
        "temperature": random() * 15,
        "pressure": random() * 20,
        "batteryRemaining": randint(0, 100),
        "isCheckpoint": random() > 0.5,
        "time": int(round(time() * 1000)),
        "imageSize": img_size
    })

def create_tripname() -> str:
    return f"trip_{int(round(time() * 1000))}"

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    img = cv2.imread("test.png")
    img_size = len(img.data)
    

    tcp.connect(IP_ADDRESS, PORT)

    # Step 1 : send the tr save request
    resp_save = send_receive(tcp, create_msg(MediatorMessageTypes.REQ_TR_SAVE, {}), MediatorMessageTypes.RESP_TR_SAVE)

    # Step 2 : send multiple images 
    NB_ITERATIONS = 20
    SEND_PERIOD = 0.1
    elapsed = 1000
    for index in range(NB_ITERATIONS):
        if elapsed < SEND_PERIOD:
            sleep(SEND_PERIOD - elapsed)
        start = time()
        # The actual process
        # TODO : do some modifications on image in order to see changes ?
        register_msg = register_message(img_size)
        resp_ack = send_receive(tcp, register_msg, MediatorMessageTypes.RESP_ACK)
        tcp.send_bytes(img.data.obj)

        end = time()
        elapsed = end - start
        print(f"Sent in {elapsed} seconds")
    
    resp_end_save = send_receive(tcp, 
        create_msg(MediatorMessageTypes.REQ_TR_END_SAVE, 
        {"tripName": create_tripname()}, 
        MediatorMessageTypes.REQ_TR_END_SAVE)
    )



if __name__ == "__main__":
    main()