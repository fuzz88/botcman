from .serializers import SerializerMixin


class ZMQServer(SerializerMixin):

    __procedures: dict = {}

    def start(self, bind_addr: str):
        pass

    def shutdown(self):
        pass

    def register(self, proc: callable, proc_name: str):
        self.__procedures[proc_name] = proc
