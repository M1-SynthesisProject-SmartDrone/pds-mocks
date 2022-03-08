from typing import Any, Tuple
from loguru import logger

from library.Message import Message
from library.UdpSocket import UdpSocket

# ==== RECEIVE ====
def receive_message(udp_socket: UdpSocket, wanted_type: str = None) -> Message:
    message = Message.fromStr(udp_socket.receive())
    if wanted_type is not None and message.type != wanted_type:
        raise ValueError(f"Didn't receive the wanted type. Expected \"{wanted_type}\" but got \"{message.type}\"")
    return message

def receive_answer(udp_socket: UdpSocket, need_positive=False) -> Message:
    message = receive_message(udp_socket, wanted_type="ANSWER")
    if need_positive and not message.content["validated"]:
        raise ValueError(f"Expecting a positive answer bu received {message}")

# ==== SEND ====
def send_answer(udp_socket: UdpSocket, msg_type: str, validated: bool, message_str: str = "") -> None:
    message = Message("ANSWER", {
        "name": msg_type, "validated": validated, "message": message_str
    })
    logger.info(f"Send answer {message}")
    udp_socket.send_as_response(message.toJsonStr())

def send_message(udp_socket: UdpSocket, message: Message, address: Tuple[str, int]) -> None:
    udp_socket.send(message.toJsonStr(), address)

def send_ack(udp_socket: UdpSocket, ip_address: str, port: int) -> None:
    message = Message("ACK", {})
    send_message(udp_socket, message, (ip_address, port))

def send_start_drone(udp_socket: UdpSocket, ip_address: str, port: int) -> None:
    message = Message("START_DRONE", {"startDrone": True})
    send_message(udp_socket, message, (ip_address, port))

def send_manual_control(udp_socket: UdpSocket, ip_address: str, port: int, x=0.0, y=0.0, z=0.0, r=0.0) -> None:
    """x, y, z & r are numbers bounded between -1 and 1
    """
    message = Message("MANUAL_CONTROL", {
        "x": x,
        "y": y,
        "z": z,
        "r": r
    })
    send_message(udp_socket, message, (ip_address, port))