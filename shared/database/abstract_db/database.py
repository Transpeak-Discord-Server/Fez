from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Any

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from shared.database.abstract_db.ban_dao import BanDAO
from shared.database.abstract_db.msgcount_dao import MsgCountDAO
from shared.database.abstract_db.role_dao import RoleDAO
from shared.database.abstract_db.user_dao import UserDAO

@dataclass
class DAOGroup:
    ban: BanDAO
    msgcount: MsgCountDAO
    role: RoleDAO
    user: UserDAO

class Database(ABC):

    def __init__(self, database_url: str) -> None:
        self._engine = create_async_engine(database_url, echo=True)
        self.async_session = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    @abstractmethod
    def ban_dao(self, session: AsyncSession) -> BanDAO: ...

    @abstractmethod
    def msgcount_dao(self, session: AsyncSession) -> MsgCountDAO: ...

    @abstractmethod
    def role_dao(self, session: AsyncSession) -> RoleDAO: ...

    @abstractmethod
    def user_dao(self, session: AsyncSession) -> UserDAO: ...

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.async_session() as session:
            try:
                yield session
            finally:
                await session.close()

    @asynccontextmanager
    async def dao_sessions(self) -> AsyncIterator[DAOGroup]:
        async with self.get_session() as session:
            yield DAOGroup(
                ban=self.ban_dao(session),
                msgcount=self.msgcount_dao(session),
                role=self.role_dao(session),
                user=self.user_dao(session),
            )

    async def __aenter__(self) -> Database:
        return self

    async def close(self) -> None:
        await self._engine.dispose()

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()