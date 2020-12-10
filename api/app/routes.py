import random
import logging
import asyncio
from typing import List


from fastapi import Depends, WebSocket
from websockets import ConnectionClosedError, ConnectionClosedOK

import models
import auth
import db


log = logging.getLogger("routes")


def init(app):
    @app.get("/movers/", response_model=List[models.API_User])
    @auth.secure()
    async def read_api_users(current_user=Depends(auth.current_user)):
        query = models.api_users.select()
        return await db.database.fetch_all(query)

    @app.post("/team/add")
    @auth.secure()
    async def add_team_member(new_mover: models.Mover, current_user=Depends(auth.current_user)):
        nm = new_mover.dict()
        nm.pop("id", None)
        query = models.temp_movers.insert(nm | {"status": "регистрация", "code": random.randint(100000000, 999999999)})
        return await db.database.execute(query)

    @app.delete("/team/archive/{id}")
    @auth.secure()
    async def archive_team_member(id: int, current_user=Depends(auth.current_user)):
        query = models.temp_movers.update().where(models.temp_movers.c.id == id).values(status="в архиве")
        return await db.database.execute(query)

    @app.get("/team", response_model=List[models.Mover])
    @auth.secure()
    async def get_all_team_members(current_user=Depends(auth.current_user)):
        query = models.temp_movers.select()
        return await db.database.fetch_all(query)

    @app.websocket("/events")
    async def websocket_endpoint(websocket: WebSocket, user=Depends(auth.get_user)):
        """
        TODO:
            - make websockets handling as separate service, without uvicorn and fastapi.
        """
        await websocket.accept()
        connected = True

        event_q = asyncio.Queue()

        def callback(q):
            def cb(connection, pid, channel, payload):
                q.put_nowait({"event": {"name": "team_members_update", "pid": pid}})
            return cb

        async with db.notify_pool.pool.acquire() as connection:
            cb = callback(event_q)
            await connection.add_listener("botcman__events", cb)

            while connected:
                event = await event_q.get()
                try:
                    await websocket.send_json(event)
                except (ConnectionClosedOK, ConnectionClosedError):
                    log.info("websocket connection was closed. cleanup.")
                    await connection.remove_listener("botcman__events", cb)
                    connected = False
