import random

from base import Base
from packet import Packet
from receiver import Receiver


class Transmitter(Base):
    def __init__(self, key: str, bait_count: int = 2, chunk_size: int = 3):
        pass

    def transmit(self, message: str, receiver: Receiver) -> list[Packet]:
        pass

    def _prepare_packets(self, message: str) -> list[Packet]:
        pass

    def _add_bait_packets(self, packets: list) -> None:
        pass
