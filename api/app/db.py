import databases
import sqlalchemy
import settings
import asyncpg


database = databases.Database(str(settings.DATABASE_URL))

metadata = sqlalchemy.MetaData()

class NotifyPool():
    async def create_pool(self, dsn):
        self.pool = await asyncpg.create_pool(dsn=dsn)

notify_pool = NotifyPool()


def init(app):
    @app.on_event("startup")
    async def startup():
        await database.connect()
        await notify_pool.create_pool(settings.DATABASE_URL)

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()
