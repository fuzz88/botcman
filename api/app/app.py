from typing import List
from fastapi import FastAPI

import models
import db

app = FastAPI()

db.init_app(app)


@app.get("/api_users/", response_model=List[models.API_User])
async def read_api_users():
    query = models.api_users.select()
    return await db.database.fetch_all(query)
