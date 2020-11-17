from typing import Any
from .base import BaseSerializer
from .exceptions import SerializerError

import pickle


class PickleSerializer(BaseSerializer):
    """ Pickle serialization for event_bus. """

    def serialize(self, data: Any) -> bytes:
        try:
            return pickle.dumps(data)
        except pickle.PicklingError:
            raise SerializerError(f'Cant pickle data: { data }')

    def deserialize(self, data: bytes) -> Any:
        try:
            return pickle.loads(data)
        except pickle.PicklingError:
            raise SerializerError(f'Cant unpickle data: { data }')
