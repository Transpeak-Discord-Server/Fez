from contextlib import asynccontextmanager
from typing import AsyncIterator

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