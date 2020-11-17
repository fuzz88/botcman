from typing import Awaitable

import asyncio
from aioredis import create_connection, Channel


class RedisWires():
    """ Communicates peers on event_bus via Redis Pub/Sub. """

    def __init__(self):
        self._pub = None
        self._sub = None
        self._channels = {}
        self._callbacks = []

    async def _connect(self, addr: str, port: int):
        #  if Redis is not connected, then lets connect it
        if self._pub is None:
            self._pub = await create_connection((addr, port))
        if self._sub is None:
            self._sub = await create_connection((addr, port))

    async def _subscribe(self, channels: list[bytes]):
        for channel_name in channels:
            #  for every given channel --- subscribe
            channel = Channel(channel_name, is_pattern=False)
            await self._sub.execute_pubsub(b'SUBSCRIBE', channel)
            self._channels |= {channel_name: channel}

    async def _register_receiver_callback(self, callback: Awaitable):
        self._callbacks.append(callback)

    async def _publish(self, channel_name: bytes, message: bytes):
        await self._pub.execute(b'PUBLISH', channel_name, message)

    async def _receiver(self):
        tasks = []
        for name, channel in self._channels.items():
            tasks.append(asyncio.ensure_future(self._wait_message(name, channel)))
        await asyncio.gather(*tasks)

    async def _wait_message(self, name, channel):
        while True:
            async for message in channel.iter():
                for cb in self._callbacks:
                    await cb(name, message)
