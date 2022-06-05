""" This script will permits to emulate the mediator behavior :
it will receive requests and send aswers accordingly to the specs
"""
from concurrent.futures import thread
from typing import Callable, Dict
from loguru import logger
import time
from random import randint
from pathlib import Path
import threading
import signal

import cv2

import sys
sys.path.append(Path(__file__).resolve().parents[1].as_posix())
# Must be put after sys.path.append
from library import * # noqa
from modes import MediatorMode
from MediatorMockInfos import MediatorMockInfos
from Thread1 import Thread1
from Thread2 import Thread2

# ==== CONSTANTS ====
PORT_1, PORT_2 = 7070, 7071

# ==== GLOBAL VARIABLES ====
infos = MediatorMockInfos()
thread1 = Thread1(PORT_1)
thread2 = Thread2(PORT_2)

# Load the image in the main folder
image = cv2.imread((Path(__file__).resolve().parent / "test.png").as_posix())
infos.image = image.tobytes()

# ==== SIGNAL HANDLER ====
def handler(signum, frame):
    logger.info("Stop threads")
    infos.is_running = False
    if thread1.tcp.com_socket is not None:
        thread1.tcp.close()
    if thread2.tcp.com_socket is not None:
        thread2.tcp.close()

def main():
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    # Catch SIGINT
    signal.signal(signal.SIGINT, handler)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()