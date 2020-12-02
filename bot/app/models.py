from typing import Optional
import sqlalchemy
import pydantic

metadata = sqlalchemy.MetaData()

bot_users = sqlalchemy.Table(
    "bot_users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(length=256)),
    sqlalchemy.Column("first_name", sqlalchemy.String(length=256)),
    sqlalchemy.Column("last_name", sqlalchemy.String(length=256)),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger),
)

avatars = sqlalchemy.Table(
    "avatars",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer),
    sqlalchemy.Column("filename", sqlalchemy.String(length=256)),
    sqlalchemy.Column("bin_data", sqlalchemy.LargeBinary),
)


class BotUserWithoutAvatar(pydantic.BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    chat_id: int


class BotUser(pydantic.BaseModel):
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    chat_id: int
    profile_photo: Optional[dict]
