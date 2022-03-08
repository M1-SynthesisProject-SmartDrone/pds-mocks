""" This script will permit to test the app without the server on :
it will receive requests and send aswers accordingly to the specs
"""
from loguru import logger
from time import sleep
import threading
from random import randint
from pathlib import Path

import sys
sys.path.append(Path(__file__).parents[1].as_posix())
# Must be put after sys.path.append
from library import * # noqa

PORT = 6869
udp_socket = UdpSocket(PORT)


def thread_receive() -> None:
    while "Thread en cours":
        message: Message = receive_message(udp_socket)
        if (message.type == "MANUAL_CONTROL"):
            logger.debug(f"Receive manual control : {message.content}")
        else:
            logger.info(f"Received message : {message}")
            if message.type == "RECORD":
                # Time for creating file, saving it
                sleep(2)
                send_answer(udp_socket, "RECORD", True)
            elif message.type == "START_DRONE":
                # Cannot do this
                send_answer(udp_socket, "START_DRONE", False, "Cannot do this !!!")


def thread_send() -> None:
    cpt = 0
    while "Thread en cours":
        sleep(1)
        if cpt % 4 == 0:
            drone_status = Message("DRONE_STATE", {"armed": True})
            logger.debug("Send drone status message")
            udp_socket.send_as_response(drone_status.toJsonStr())
            cpt = 0
        else:
            # Create random drone data message
            drone_data = Message("DRONE_DATA", {
                "batteryRemaining": randint(0, 100),
                "lat": randint(100000000, 500000000),
                "lon": randint(100000000, 500000000),
                "alt": randint(1000, 2000),
                "relativeAlt": randint(100, 200),
                "vx": randint(0, 50),
                "vy": randint(0, 50),
                "vz": randint(0, 50),
                "yawRotation": randint(0, 364)
            })
            # This message is not so important
            logger.debug("Send drone update")
            udp_socket.send_as_response(drone_data.toJsonStr())
        cpt += 1

def main():
    print("Wait for ack request")
    ack_msg = receive_message("ACK")
    sleep(0.1)
    send_answer(udp_socket, "ACK", True)

    start_msg = receive_message("START_DRONE")
    send_answer(udp_socket, "START_DRONE", True)

    # Those threads run forever
    thread_recv = threading.Thread(target=thread_receive)
    thread_snd = threading.Thread(target=thread_send)
    thread_recv.start()
    thread_snd.start()
    for t in (thread_recv, thread_snd):
        t.join()

if __name__ == "__main__":
    main()
