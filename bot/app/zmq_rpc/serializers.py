from typing import Any
from .base import RPCSerializer


class MsgPackRPCSerializer(RPCSerializer):

    def serialize(self, data: Any) -> bytes:
        pass

    def deserialize(self, data: bytes) -> Any:
        pass
