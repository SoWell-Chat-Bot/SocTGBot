import asyncpg
from os import getenv

from asyncpg import RaiseError
from dotenv import load_dotenv

load_dotenv()

async def load_data():
    try:
        conn = await asyncpg.connect(
            host=getenv('DB_HOST'),
            port=getenv('DB_PORT'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASSWORD'),
            database=getenv('DB_NAME')
        )
        print("Подключен к ДБ")

        rows = await conn.fetch("SELECT * FROM tasks")

        return rows
    except:
        print("Проблемы с загрузкой данных")
        return False

