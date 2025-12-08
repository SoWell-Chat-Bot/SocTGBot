import asyncpg
from os import getenv


class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=getenv('DB_HOST'),
            port=getenv('DB_PORT'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASSWORD'),
            database=getenv('DB_NAME')
        )
        print("База данных подключена")

    async def get_random_task(self):
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM tasks TABLESAMPLE SYSTEM (1) LIMIT 1"
            )
            if not row:
                row = await conn.fetchrow(
                    "SELECT * FROM tasks ORDER BY RANDOM() LIMIT 1"
                )
            return row

    async def close(self):
        if self.pool:
            await self.pool.close()


