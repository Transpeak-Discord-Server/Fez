from typing import Iterable, Optional, LiteralString
import psycopg


class Database:

    def __init__(self, conn_info: str):
        self.connection: Optional[psycopg.AsyncConnection] = None
        self.conn_info = conn_info


    async def __aenter__(self):
        self.connection = await psycopg.AsyncConnection.connect(self.conn_info)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type is None:
                await self.connection.commit()
            else:
                await self.connection.rollback()
            await self.connection.close()

    # Should be used for INSERT, UPDATE, DELETE, etc.
    async def execute(self, query: LiteralString, *args) -> int:
        if not self.connection:
            raise psycopg.ProgrammingError("Database connection not established, use 'async with' statement")
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, *args)
            return cursor.rowcount

    # Should be used for SELECT
    async def fetchall(self, query: LiteralString, *args) -> Iterable:
        if not self.connection:
            raise psycopg.ProgrammingError("Database connection not established, use 'async with' statement")
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, *args)
            return await cursor.fetchall()

    # Should be used for SELECT
    async def fetchone(self, query: LiteralString, *args):
        if not self.connection:
            raise psycopg.ProgrammingError("Database connection not established, use 'async with' statement")
        async with self.connection.cursor() as cursor:
            await cursor.execute(query, *args)
            return await cursor.fetchone()