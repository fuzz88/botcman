import redis


class RedisWires:
    """ Communicates peers on event_bus via Redis Pub/Sub. """

    def __init__(self):
        self._redis = None
        self._connection_pool = None
        self._pubsub = None
        self._ps_thread = None
        self._channels = {}
        self._callbacks = []

    def connect(self, url: str):
        #  if Redis is not connected, then lets connect it
        if self._connection_pool is None:
            self._connection_pool = redis.BlockingConnectionPool.from_url(
                url, max_connections=10, timeout=5
            )
        if self._redis is None:
            self._redis = redis.Redis(connection_pool=self._connection_pool)

        if self._pubsub is None:
            self._pubsub = self._redis.pubsub()

    def disconnect(self):
        self._redis = None
        self._pubsub = None
        self._connection_pool = None

    def subscribe(self, channels: dict):
        for channel, handler in channels.items():
            self._pubsub.subscribe(**{channel: handler})

    def publish(self, channel_name: bytes, message: bytes):
        self._redis.publish(channel_name, message)

    def start(self):
        self._ps_thread = self._pubsub.run_in_thread()

    def stop(self):
        self._ps_thread.stop()
