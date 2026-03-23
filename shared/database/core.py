from sqlite3 import Row
from typing import Iterable

import aiosqlite
import os

DATABASE_FOLDER = os.path.join(os.path.dirname(__file__), 'dbfiles')

class Database:

    def __init__(self, database_name: str):
        self.connection = None
        self.database_name = database_name
        self.database_path = os.path.join(DATABASE_FOLDER, database_name)

    async def __aenter__(self):
        self.connection = await aiosqlite.connect(self.database_path)
        self.connection.row_factory = aiosqlite.Row
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                await self.connection.commit()
            await self.connection.close()

    async def connect(self):
        await self.__aenter__()

    async def disconnect(self):
        await self.__aexit__(None, None, None)

    # Should be used for INSERT, UPDATE, DELETE, etc.
    async def execute(self, query: str, *args) -> int:
        async with self.connection.execute(query, *args) as cursor:
            await self.connection.commit()
            return cursor.rowcount

    # Should be used for SELECT
    async def fetchall(self, query: str, *args) -> Iterable[Row]:
        async with self.connection.execute(query, *args) as cursor:
            return await cursor.fetchall()

    # Should be used for SELECT
    async def fetchone(self, query: str, *args) -> Row:
        async with self.connection.execute(query, *args) as cursor:
            return await cursor.fetchone()