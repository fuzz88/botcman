import random
import logging
import asyncio
from typing import List


from fastapi import Depends, WebSocket
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

import models
import auth
import db

logging.basicConfig(level=logging.INFO)
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

    @app.delete("/team/delete/{id}")
    @auth.secure()
    async def delete_team_member(id: int, current_user=Depends(auth.current_user)):
        query = models.temp_movers.update().where(models.temp_movers.c.id == id).values(status="удалён")
        return await db.database.execute(query)

    @app.get("/team", response_model=List[models.Mover])
    @auth.secure()
    async def get_all_team_members(current_user=Depends(auth.current_user)):
        query = models.temp_movers.select()
        return await db.database.fetch_all(query)

    @app.websocket("/events")
    async def websocket_endpoint(websocket: WebSocket, user=Depends(auth.get_user)):
        await websocket.accept()
        connected = True

        def callback(ws):
            def cb(connection, pid, channel, payload):
                try:
                    asyncio.ensure_future(
                        ws.send_json({"event": {"name": "team_members_update", "pid": pid}})
                    )
                except (ConnectionClosedOK, ConnectionClosedError):
                    connected = False
                    log.info(f"Client disconnected {ws}")
            return cb

        async with db.notify_pool.pool.acquire() as connection:
            await connection.add_listener("botcman__events", callback(websocket))

            while connected:
                async with connection.transaction():
                    await asyncio.sleep(0.1)
