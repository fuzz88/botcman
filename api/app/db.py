import databases
import sqlalchemy


DATABASE_URL = "postgresql://postgres:postgres@localhost/botcman__test"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()


def init_app(app):
    @app.on_event("startup")
    async def startup():
        await database.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await database.disconnect()
