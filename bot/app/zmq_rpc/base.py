"""

Этот файл содержит, в основном, описание интерфейсов различных частей
системы вызовов удаленных процедур.

Если возвращаемое значение метода класса не аннотировано явно,
можете смело предположить, что метод не должен ничего возвращать.

"""

from .serializers import MsgPackRPCSerializer
from abc import ABC, abstractmethod
from typing import Any, Optional


class RPCSerializer(ABC):
    """ Base class """
    @abstractmethod
    def serialize(self, data: Any) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        pass


class SerializerMixin:
    """
    Mixin adds serialization both to RPCClient and RPCServer.

    Default serizalizer is [MsgPack](https://github.com/msgpack/msgpack-python)

    """
    __serializer: RPCSerializer

    def __init__(self, serializer: RPCSerializer = None):
        if serializer is None:
            self.__serializer = MsgPackRPCSerializer()
        else:
            self.__serializer = serializer


class RPCClient(ABC, SerializerMixin):
    """ Base class """
    @abstractmethod
    def connect(self, addr: str):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def call(self, proc_name: str, kwargs: dict) -> Optional:
        pass


class RPCServer(ABC, SerializerMixin):
    """ Base class """
    @abstractmethod
    def start(self, bind_addr: str):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def register(self, proc: callable, proc_name: str):
        pass
