import databases
import sqlalchemy
import settings
import asyncpg

database = databases.Database(str(settings.DATABASE_URL))

metadata = sqlalchemy.MetaData()


def init(app):

    # setup fastapi events

    @app.on_event("startup")
    async def startup():
        await database.connect()  # databases
        await postgres_connections.create_pool(settings.DATABASE_URL)  # asyncpg, for postgres NOTIFY

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()


class DBPool:
    async def create_pool(self, dsn):
        self.pool = await asyncpg.create_pool(dsn=dsn)


# stuff below ▼ can be imported literally everywhere

# inits asyncpg on fastapi startup
postgres_connections = DBPool()

# sqlalchemy table models

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
