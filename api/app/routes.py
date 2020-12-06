import random
from typing import List


from fastapi import Depends

import models
import auth
import db


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
        query = models.temp_movers.insert(
            nm | {"status": "регистрация", "code": random.randint(100000000, 999999999)}
        )
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
