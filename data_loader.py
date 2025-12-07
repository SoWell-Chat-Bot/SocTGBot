import asyncpg
from os import getenv

from dotenv import load_dotenv

load_dotenv()

async def connect_db():
    try:
        conn = await asyncpg.connect(
            host=getenv('DB_HOST'),
            port=getenv('DB_PORT'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASSWORD'),
            database=getenv('DB_NAME')
        )
        return conn
    except:
        print("Проблемы с загрузкой данных")
        return False

async def load_random_task(conn):
    query = "SELECT * FROM tasks TABLESAMPLE SYSTEM (1) LIMIT 1"
    row = await conn.fetchrow(query)
    if row is None:
        row = await conn.fetchrow(
            "SELECT * FROM tasks ORDER BY RANDOM() LIMIT 1"
        )
    return dict(row)


