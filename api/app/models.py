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


class Job(BaseModel):
    id: Optional[int]
    ext_id: int
    manager: str
    chat_message: str
    brigadier_message: str
    mover_message: str
    courier_message: str
    brigade: Optional[str]
    status: str

class JobInList(BaseModel):
    id: int
    ext_id: int
    manager: str
    brigadier: Optional[str]
    brigade: Optional[str]
    status: str


movers = sqlalchemy.Table(
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

jobs = sqlalchemy.Table(
    "temp_jobs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("ext_id", sqlalchemy.Integer),
    sqlalchemy.Column("manager_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("managers.id")),
    sqlalchemy.Column("brigade_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("temp_brigades.id")),
    sqlalchemy.Column("messages_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("temp_messages.id")),
    sqlalchemy.Column("status", sqlalchemy.String),
)

messages = sqlalchemy.Table(
    "temp_messages",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("chat_message", sqlalchemy.String),
    sqlalchemy.Column("brigadier_message", sqlalchemy.String),
    sqlalchemy.Column("mover_message", sqlalchemy.String),
    sqlalchemy.Column("courier_message", sqlalchemy.String),
)

managers = sqlalchemy.Table(
    "managers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)

brigades = sqlalchemy.Table(
    "temp_brigades",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("brigade", sqlalchemy.dialects.postgresql.JSONB),
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
