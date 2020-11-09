from typing import Any
from .base import RPCSerializer


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


class MsgPackRPCSerializer(RPCSerializer):

    def serialize(self, data: Any) -> bytes:
        pass

    def deserialize(self, data: bytes) -> Any:
        pass
