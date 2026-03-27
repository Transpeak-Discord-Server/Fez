from typing import Iterable, Optional, LiteralString
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv
import os
PROJECT_PATH = os.path.join(os.path.dirname(__file__), '../..')
load_dotenv(dotenv_path= os.path.join(PROJECT_PATH, '.env'))

class Database:

    _pool: Optional[AsyncConnectionPool] = None

    @classmethod
    async def initialise(cls, conn_info: str = os.getenv("DATABASE_INFO")):
        if not conn_info:
            raise ValueError("Database connection info not found in .env file.")
        cls._pool = AsyncConnectionPool(
            conninfo=conn_info,
            open=False,
            kwargs={"row_factory": dict_row}
        )
        await cls._pool.open()

    @classmethod
    async def close(cls):
        if cls._pool:
            await cls._pool.close()

    # Should be used for INSERT, UPDATE, DELETE, etc.
    async def execute(self, query: LiteralString, *args) -> int:
        if not self._pool:
            raise RuntimeError("Database pool not established, use Database.initialise() first.")
        async with self._pool.connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, *args)
                return cursor.rowcount

    # Should be used for SELECT
    async def fetchall(self, query: LiteralString, *args) -> Iterable:
        if not self._pool:
            raise RuntimeError("Database pool not established, use Database.initialise() in bot startup.")
        async with self._pool.connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, *args)
                return await cursor.fetchall()

    # Should be used for SELECT
    async def fetchone(self, query: LiteralString, *args):
        if not self._pool:
            raise RuntimeError("Database pool not established, use Database.initialise() first.")
        async with self._pool.connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, *args)
                return await cursor.fetchone()