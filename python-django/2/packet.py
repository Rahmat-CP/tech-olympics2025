from dataclasses import dataclass
from typing import Callable


@dataclass
class Packet:
    # TODO: Implement fields

    def is_valid(self, hash_func: Callable, key: str) -> bool:
        pass