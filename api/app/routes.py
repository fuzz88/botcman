from typing import List

from fastapi import Depends

from fastapi.middleware.cors import CORSMiddleware

import models
import auth
import db

origins = [
    "http://localhost:5000",
]


def init(app):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api_users/", response_model=List[models.API_User])
    @auth.secure()
    async def read_api_users(current_user=Depends(auth.current_user)):

        query = models.api_users.select()
        return await db.database.fetch_all(query)
