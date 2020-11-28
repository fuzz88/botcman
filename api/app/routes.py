from typing import List

from fastapi import Depends

import models
import auth
import db


def init(app):
    @app.get("/api_users/", response_model=List[models.API_User])
    @auth.secure()
    async def read_api_users(current_user=Depends(auth.current_user)):

        query = models.api_users.select()
        return await db.database.fetch_all(query)
