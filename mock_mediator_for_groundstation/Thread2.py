
import threading

from library.TcpSocket import TcpSocket
from MediatorMockInfos import MediatorMockInfos

# ==== THREAD SECONDARY PORT ====
class Thread2 (threading.Thread):
    def __init__(self, port: int) -> None:
        threading.Thread.__init__(self)
        self.port: int = port
        self.tcp = TcpSocket()
        self.infos = MediatorMockInfos()
    
    def run(self) -> None:
        # self.tcp.wait_connection(self.port)
        while self.infos.is_running:
            pass