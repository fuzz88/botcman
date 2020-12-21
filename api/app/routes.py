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
    @app.get("/jobs/list", response_model=List[models.JobInList])
    @auth.secure()
    async def get_all_jobs(current_user=Depends(auth.current_user)):
        return await db.database.fetch_all(
            (
                models.jobs.join(models.managers)
                .join(models.messages)
                .join(models.brigades)
                .select()
                .with_only_columns(
                    [
                        models.jobs.c.id,
                        models.managers.c.name.label("manager"),
                        models.jobs.c.ext_id,
                        models.brigades.c.brigade[("brigadier")].label("brigadier"),
                        models.jobs.c.status,
                    ]
                )
            )
        )

    @app.get("/jobs/get/{id}", response_model=models.Job)
    @auth.secure()
    async def get_job(id: int, current_user=Depends(auth.current_user)):
        return await db.database.fetch_one(
            models.jobs.join(models.managers)
            .join(models.messages)
            .select()
            .where(models.jobs.c.id == id)
            .with_only_columns(
                [
                    models.jobs.c.id,
                    models.jobs.c.ext_id,
                    models.jobs.c.status,
                    models.managers.c.name.label("manager"),
                    models.messages.c.chat_message,
                    models.messages.c.brigadier_message,
                    models.messages.c.mover_message,
                    models.messages.c.courier_message,
                ]
            )
        )

    @app.post("/jobs/add")
    @auth.secure()
    async def add_job(new_job: models.Job, current_user=Depends(auth.current_user)):
        job = new_job.dict()
        job.pop("id", None)
        manager_id = await db.database.fetch_val(
            models.managers.select().where(models.managers.c.name.like(job.pop("manager")))
        )
        new_job = {"ext_id": job.pop("ext_id"), "manager_id": manager_id}
        messages_id = await db.database.execute(models.messages.insert(job))
        new_job |= {"messages_id": messages_id}
        return await db.database.execute(models.jobs.insert(new_job))

    @app.post("/jobs/edit/{id}")
    @auth.secure()
    async def edit_job(id: int, edit_job: models.Job, current_user=Depends(auth.current_user)):
        new_job = edit_job.dict()
        new_job.pop("id", None)
        new_job.pop("brigade", None)
        old_job = await db.database.fetch_one(models.jobs.select().where(models.jobs.c.id == id))
        manager_id = await db.database.fetch_val(
            models.managers.select().where(models.managers.c.name.like(new_job.pop("manager")))
        )
        new_job |= {"manager_id": manager_id}
        messages = {
            "chat_message": new_job.pop("chat_message"),
            "brigadier_message": new_job.pop("brigadier_message"),
            "mover_message": new_job.pop("mover_message"),
            "courier_message": new_job.pop("courier_message"),
        }
        await db.database.execute(
            models.messages.update().where(models.messages.c.id == old_job["messages_id"]).values(messages)
        )
        return await db.database.execute(models.jobs.update().where(models.jobs.c.id == id).values(new_job))

    @app.delete("/jobs/archive/{id}")
    @auth.secure()
    async def archive_jobs(id: int, current_user=Depends(auth.current_user)):
        return await db.database.execute(models.jobs.update().where(models.jobs.c.id == id).values(status="в архиве"))

    @app.get("/team/list", response_model=List[models.Mover])
    @auth.secure()
    async def get_all_team_members(current_user=Depends(auth.current_user)):
        return await db.database.fetch_all(models.movers.select())

    @app.post("/team/add")
    @auth.secure()
    async def add_team_member(new_mover: models.Mover, current_user=Depends(auth.current_user)):
        nm = new_mover.dict()
        nm.pop("id", None)
        return await db.database.execute(
            models.movers.insert(nm | {"status": "регистрация", "code": random.randint(100000000, 999999999)})
        )

    @app.delete("/team/archive/{id}")
    @auth.secure()
    async def archive_team_member(id: int, current_user=Depends(auth.current_user)):
        return await db.database.execute(
            models.movers.update().where(models.movers.c.id == id).values(status="в архиве")
        )

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
