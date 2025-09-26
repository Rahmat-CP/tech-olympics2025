from base import Base
from packet import Packet


class Receiver(Base):
    def __init__(self, key: str):
        pass

    def receive(self, packets: list[Packet]) -> None:
        pass

    def get_message(self) -> str:
        pass
