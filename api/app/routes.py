import random
import logging
import asyncio
import json
from typing import List


from fastapi import Depends, WebSocket
from websockets import ConnectionClosedError, ConnectionClosedOK

from db import database, postgres_connections, jobs, managers, brigades, messages, movers
from models import JobInList, Job, Mover
import auth


log = logging.getLogger("routes")


def init(app):
    @app.get("/jobs/list", response_model=List[JobInList])
    @auth.secure()
    async def get_all_jobs(current_user=Depends(auth.current_user)):
        return await database.fetch_all(
            (
                jobs.join(managers)
                .join(messages)
                .join(brigades)
                .select()
                .with_only_columns(
                    [
                        jobs.c.id,
                        managers.c.name.label("manager"),
                        jobs.c.ext_id,
                        brigades.c.brigade[("brigadier")].label("brigadier"),
                        jobs.c.status,
                    ]
                )
            )
        )

    @app.get("/jobs/get/{id}", response_model=Job)
    @auth.secure()
    async def get_job(id: int, current_user=Depends(auth.current_user)):
        return await database.fetch_one(
            jobs.join(managers)
            .join(messages)
            .select()
            .where(jobs.c.id == id)
            .with_only_columns(
                [
                    jobs.c.id,
                    jobs.c.ext_id,
                    jobs.c.status,
                    managers.c.name.label("manager"),
                    messages.c.chat_message,
                    messages.c.brigadier_message,
                    messages.c.mover_message,
                    messages.c.courier_message,
                ]
            )
        )

    @app.post("/jobs/add")
    @auth.secure()
    async def add_job(new_job: Job, current_user=Depends(auth.current_user)):
        job = new_job.dict()
        job.pop("id", None)
        manager_id = await database.fetch_val(managers.select().where(managers.c.name.like(job.pop("manager"))))
        new_job = {"ext_id": job.pop("ext_id"), "manager_id": manager_id}
        messages_id = await database.execute(messages.insert(job))
        new_job |= {"messages_id": messages_id}
        return await database.execute(jobs.insert(new_job))

    @app.post("/jobs/edit/{id}")
    @auth.secure()
    async def edit_job(id: int, edit_job: Job, current_user=Depends(auth.current_user)):
        new_job = edit_job.dict()
        new_job.pop("id", None)
        new_job.pop("brigade", None)
        old_job = await database.fetch_one(jobs.select().where(jobs.c.id == id))
        manager_id = await database.fetch_val(managers.select().where(managers.c.name.like(new_job.pop("manager"))))
        new_job |= {"manager_id": manager_id}

        await database.execute(
            messages.update()
            .where(messages.c.id == old_job["messages_id"])
            .values(
                {
                    message_type: new_job.pop(message_type)
                    for message_type in ["chat_message", "brigadier_message", "mover_message", "courier_message"]
                }
            )
        )
        await database.execute(jobs.update().where(jobs.c.id == id).values(new_job))
        return {"status": "done"}

    @app.delete("/jobs/archive/{id}")
    @auth.secure()
    async def archive_jobs(id: int, current_user=Depends(auth.current_user)):
        return await database.execute(jobs.update().where(jobs.c.id == id).values(status="в архиве"))

    @app.get("/jobs/run/{id}")
    @auth.secure()
    async def run_job(id: int, current_user=Depends(auth.current_user)):
        status = await database.fetch_val(jobs.select().where(jobs.c.id == id).with_only_columns([jobs.c.status]))
        #  TODO: where to place is_new
        if status == "новая":
            await database.execute(jobs.update().where(jobs.c.id == id).values(status="опрос чата"))

    @app.get("/team/list", response_model=List[Mover])
    @auth.secure()
    async def get_all_team_members(current_user=Depends(auth.current_user)):
        return await database.fetch_all(movers.select())

    @app.post("/team/add")
    @auth.secure()
    async def add_team_member(new_mover: Mover, current_user=Depends(auth.current_user)):
        nm = new_mover.dict()
        nm.pop("id", None)
        return await database.execute(
            movers.insert(nm | {"status": "регистрация", "code": random.randint(100000000, 999999999)})
        )

    @app.delete("/team/archive/{id}")
    @auth.secure()
    async def archive_team_member(id: int, current_user=Depends(auth.current_user)):
        return await database.execute(movers.update().where(movers.c.id == id).values(status="в архиве"))

    @app.websocket("/events")
    async def websocket_endpoint(websocket: WebSocket, _=Depends(auth.check_coockie)):
        # handles websockets. the buggy way, actually.
        # buggy, because if you will update browser's tab, you recreate websocket each time.
        # but this handler flushes the inactive websockets the one way: when new postgres event have been came.
        # so, here we are, with little memory leakage.
        # websocket protocol is handled in uvicorn, and i didn't find the way to get connection status.
        # it have never been checked here. if we can't send with that websocket, then halt serving it,
        # but between sending messages this handler
        # (maybe disconnected and needed to be garbage-collected)
        # hangs in memory waiting for postgres event.

        await websocket.accept()
        connected = True

        event_q = asyncio.Queue()

        def callback(q):
            def cb(connection, pid, channel, payload):
                p = json.loads(payload)
                if p["table"] == "temp_movers":
                    q.put_nowait({"event": {"name": "team_members_update", "pid": pid}})
                if p["table"] == "temp_jobs":
                    q.put_nowait({"event": {"name": "jobs_update", "pid": pid}})

            return cb

        async with postgres_connections.pool.acquire() as connection:
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
