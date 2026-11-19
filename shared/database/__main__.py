import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from shared.database.BanDAO import BanDAO


class Database:

    engine: AsyncEngine
    async_session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, url: URL):
        self.engine = create_async_engine(url)
        self.async_session_maker = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    @staticmethod
    def ban_dao(session: AsyncSession) -> BanDAO:
        return BanDAO(session)

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.async_session_maker() as session:
            try:
                yield session
            finally:
                await session.close()

env_path = Path(__file__) / ".." / ".." / ".env"
env = load_dotenv(env_path)

def get_database() -> Database:
    db_url_username = os.getenv("DB_USERNAME")
    db_url_password = os.getenv("DB_PASSWORD")
    db_url_host = os.getenv("DB_HOST")
    db_url_database = os.getenv("DB_DATABASE")
    db_url = URL.create(
        "postgresql+psycopg",
        username=db_url_username,
        password=db_url_password,
        host=db_url_host,
        database=db_url_database)
    return Database(db_url)