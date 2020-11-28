from abc import ABC, abstractmethod
from typing import Any


class BaseSerializer(ABC):
    """
    Base class for event_bus serializers.
    Serialization needed to send event objects over wires.

    """

    @abstractmethod
    def serialize(self, data: Any) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        pass
