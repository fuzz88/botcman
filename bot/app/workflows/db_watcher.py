import logging
import asyncio

from aiotg import Bot, Chat

import config

from .db import get_db
from .utils import process_event


log = logging.getLogger(__name__)


async def main():
    """
    receives and processes postgres notifications.
    """
    event_q = asyncio.Queue()
    db = await get_db()

    def callback(q):
        def cb(connection, pid, channel, payload):
            q.put_nowait(payload)
        return cb

    connected = True
    async with db.pool.acquire() as connection:
        cb = callback(event_q)
        await connection.add_listener("botcman__events", cb)

        while connected:
            event = await event_q.get()
            log.info(event)
            await process_event(event)


def run():
    log.debug("database watcher is going to run...")
    asyncio.run(main())
