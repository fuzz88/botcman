from pydantic import BaseModel
import sqlalchemy

from db import metadata


class API_User(BaseModel):
    id: int
    username: str
    password: str
    role: str


api_users = sqlalchemy.Table(
    "api_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("role", sqlalchemy.String),  # enum in db, actually
)
