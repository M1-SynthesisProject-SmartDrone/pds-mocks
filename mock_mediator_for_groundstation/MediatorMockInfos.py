
from util.MetaSingleton import MetaSingleton
from modes import MediatorMode

class MediatorMockInfos(metaclass=MetaSingleton):
    """A singleton class permitting to sharing infos between threads
    """

    def __init__(self) -> None:
        self.is_running = True
        self.mode = MediatorMode.IDLE
        self.last_image_received = bytearray()
        self.current_tr_id = -1
        self.current_checkpoint_index = 0
        self.image: bytes = None