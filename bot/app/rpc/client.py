from .serializers import SerializerMixin


class ZMQClient(SerializerMixin):

    def connect(self, addr: str):
        pass

    def disconnect(self):
        pass

    def call(self, proc_name: str, kwargs: dict):
        pass
