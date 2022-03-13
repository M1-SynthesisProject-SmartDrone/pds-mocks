from typing import Any, Tuple
from loguru import logger

from library.Message import Message
from library.MessageTypes import MessageTypes
from library.UdpSocket import UdpSocket

# ==== MAIN ====
def send_receive(
    udp_socket: UdpSocket, 
    message: Message, 
    wanted_type: MessageTypes, 
    address: Tuple[str, int]) -> Message:

    """ Send a message and wait for the answer
    """
    udp_socket.send(message.toJsonStr(), address)
    response = receive_message(udp_socket, wanted_type)
    return response

# ==== RECEIVE ====
def receive_message(udp_socket: UdpSocket, wanted_type: MessageTypes = None) -> Message:
    message = Message.fromStr(udp_socket.receive())
    if wanted_type is not None and message.type != wanted_type:
        raise ValueError(f"Didn't receive the wanted type. Expected {wanted_type} but got {message.type}")
    return message

# ==== SEND ====
def send_message(udp_socket: UdpSocket, message: Message, address: Tuple[str, int]) -> None:
    udp_socket.send(message.toJsonStr(), address)

# ===== CREATE MESSAGES ====

def create_ack() -> Message:
    return Message(MessageTypes.REQ_ACK, {})

def create_drone_infos() -> Message:
    return Message(MessageTypes.REQ_DRONE_INFOS, {})

def create_start_drone() -> Message:
    return Message(MessageTypes.REQ_START_DRONE, {"startDrone": True})

def create_manual_control(x=0.0, y=0.0, z=0.0, r=0.0) -> Message:
    return Message(MessageTypes.REQ_MANUAL_CONTROL, {
        "x": x,
        "y": y,
        "z": z,
        "r": r
    })