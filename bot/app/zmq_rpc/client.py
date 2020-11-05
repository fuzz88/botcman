from .base import RPCClient

class ZMQRPCClient(RPCClient):

    def connect(self, addr: str):
        pass

    def disconnect(self):
        pass

    def call(self, proc_name: str, kwargs: dict):
        pass
