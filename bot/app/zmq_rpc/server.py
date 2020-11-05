from .base import RPCServer


class ZMQRPCServer(RPCServer):

    def start(self, bind_addr: str):
        pass

    def shutdown(self):
        pass

    def register(self, proc: callable, proc_name: str):
        pass
