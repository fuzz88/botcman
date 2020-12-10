import sqlalchemy
from typing import Optional
from pydantic import BaseModel, validator

from db import metadata


class UserCredentials(BaseModel):
    username: str
    password: str


class API_User(BaseModel):
    id: int
    username: str
    password: str
    role: str


class AuthUser(BaseModel):
    username: str
    role: str


class Mover(BaseModel):
    id: Optional[int]
    fullname: str
    experience: int
    stamina: int
    reliability: int
    code: Optional[int]
    status: Optional[str]

    @validator("fullname")
    def must_contain_3_words(cls, v):
        if len(v.split(" ")) != 3:
            raise ValueError("должно состоять из трёх слов")
        return v.title()

    @validator("experience", "stamina", "reliability")
    def must_be_number(cls, v):
        if not (isinstance(v, int) and v >= 0):
            raise ValueError("должно быть положительным числом, или 0")
        return v


temp_movers = sqlalchemy.Table(
    "temp_movers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("fullname", sqlalchemy.String),
    sqlalchemy.Column("stamina", sqlalchemy.Integer),
    sqlalchemy.Column("experience", sqlalchemy.Integer),
    sqlalchemy.Column("reliability", sqlalchemy.Integer),
    sqlalchemy.Column("code", sqlalchemy.Integer),
    sqlalchemy.Column("bot_id", sqlalchemy.Integer),
    sqlalchemy.Column("status", sqlalchemy.String),
)


api_users = sqlalchemy.Table(
    "api_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("role", sqlalchemy.String),
)

bot_users = sqlalchemy.Table(
    "bot_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("chat_id", sqlalchemy.Integer),
)

avatars = sqlalchemy.Table(
    "avatars",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer),
    sqlalchemy.Column("filename", sqlalchemy.String),
    sqlalchemy.Column("bin_data", sqlalchemy.Binary),
)

movers = sqlalchemy.Table(
    "movers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("fullname", sqlalchemy.String),
    sqlalchemy.Column("bot_user_id", sqlalchemy.Integer),
)

movers_stats = sqlalchemy.Table(
    "movers_stats",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("mover_id", sqlalchemy.Integer),
    sqlalchemy.Column("stamina", sqlalchemy.Integer),
    sqlalchemy.Column("experience", sqlalchemy.Integer),
    sqlalchemy.Column("activity", sqlalchemy.Integer),
)

mover_code = sqlalchemy.Table(
    "mover_code",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("code", sqlalchemy.Integer),
    sqlalchemy.Column("mover_id", sqlalchemy.Integer),
)
