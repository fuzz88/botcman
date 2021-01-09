import asyncpg
import config


class DBPool:
    # небольшой класс, инкапсулирует ссылку на пул соединений с базой данных,
    pool = None

    # предоставляет интерфейс инициализации этого пула.
    async def create_pool(self, dsn):
        self.pool = await asyncpg.create_pool(dsn=dsn)


# в пространстве имён модуля инициализируем экзэмпляр вышеуказанного класса.
db = DBPool()


# предоставляем другим модулям интерфейс для получения доступа к вышеуказанному экземпляру.
async def get_db():
    if db.pool is None:
        await db.create_pool(config.DATABASE_URL)
    return db
