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
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            await self.connection.close()

    async def execute(self, query: str, *args) -> aiosqlite.Cursor:
        cursor = await self.connection.execute(query, *args)
        return cursor

    async def commit(self):
        await self.connection.commit()