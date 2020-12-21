import asyncpg
import config


class DBPool:
    pool = None

    async def create_pool(self, dsn):
        self.pool = await asyncpg.create_pool(dsn=dsn)


db = DBPool()


async def get_db():
    if db.pool is None:
        await db.create_pool(config.DATABASE_URL)
    return db
