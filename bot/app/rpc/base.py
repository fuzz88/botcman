from abc import ABC, abstractmethod
from typing import Any


class RPCSerializer(ABC):
    """ Base class """
    @abstractmethod
    def serialize(self, data: Any) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        pass
