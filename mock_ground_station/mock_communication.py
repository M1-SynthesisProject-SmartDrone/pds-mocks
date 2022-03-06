""" This script will permit to test the app without the server on :
it will receive requests and send aswers accordingly to the specs
"""
from loguru import logger
from time import sleep
import threading
from random import randint

from UdpSocket import UdpSocket
from Message import Message

PORT = 6869
udp_socket = UdpSocket(PORT)

def receive_message(wanted_type: str = None) -> Message:
    message = Message.fromStr(udp_socket.receive())
    if wanted_type is not None and message.type != wanted_type:
        raise ValueError(f"Didn't receive the wanted type. Expected \"{wanted_type}\" but got \"{message.type}\"")
    return message

def send_answer(msg_type: str, validated: bool, message_str: str = "") -> None:
    message = Message("ANSWER", {
        "name": msg_type, "validated": validated, "message": message_str
    })
    logger.info(f"Send answer {message}")
    udp_socket.send_as_response(message.toJsonStr())


def thread_receive() -> None:
    while "Thread en cours":
        message = receive_message()
        if (message.type == "MANUAL_CONTROL"):
            logger.debug(f"Receive manual control : {message.content}")
        else:
            logger.info(f"Received message : {message}")
            if message.type == "RECORD":
                # Time for creating file, saving it
                sleep(2)
                send_answer("RECORD", True)
            elif message.type == "START_DRONE":
                # Cannot do this
                send_answer("START_DRONE", False, "Cannot do this !!!")


def thread_send() -> None:
    cpt = 0
    while "Thread en cours":
        sleep(1)
        if cpt % 4 == 0:
            drone_status = Message("DRONE_STATUS", {"armed": True})
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
    send_answer("ACK", True)

    start_msg = receive_message("START_DRONE")
    send_answer("START_DRONE", True)

    # Those threads run forever
    thread_recv = threading.Thread(target=thread_receive)
    thread_snd = threading.Thread(target=thread_send)
    thread_recv.start()
    thread_snd.start()
    for t in (thread_recv, thread_snd):
        t.join()

if __name__ == "__main__":
    main()