import databases
import sqlalchemy
import settings


database = databases.Database(str(settings.DATABASE_URL))

metadata = sqlalchemy.MetaData()


def init(app):
    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()
