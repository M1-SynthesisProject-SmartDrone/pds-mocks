from loguru import logger

from library.Message import Message
from library.UdpSocket import UdpSocket

def receive_message(udp_socket: UdpSocket, wanted_type: str = None) -> Message:
    message = Message.fromStr(udp_socket.receive())
    if wanted_type is not None and message.type != wanted_type:
        raise ValueError(f"Didn't receive the wanted type. Expected \"{wanted_type}\" but got \"{message.type}\"")
    return message

def send_answer(udp_socket: UdpSocket, msg_type: str, validated: bool, message_str: str = "") -> None:
    message = Message("ANSWER", {
        "name": msg_type, "validated": validated, "message": message_str
    })
    logger.info(f"Send answer {message}")
    udp_socket.send_as_response(message.toJsonStr())