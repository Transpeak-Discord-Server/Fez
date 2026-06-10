from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.abstract_db.ban_dao import BanDAO
from shared.database.abstract_db.msgcount_dao import MsgCountDAO
from shared.database.abstract_db.role_dao import RoleDAO
from shared.database.abstract_db.user_dao import UserDAO


class Database(ABC):

    @abstractmethod
    async def get_ban_dao(self, session: AsyncSession) -> BanDAO: ...

    @abstractmethod
    async def get_msgcount_dao(self, session: AsyncSession) -> MsgCountDAO: ...

    @abstractmethod
    async def get_role_dao(self, session: AsyncSession) -> RoleDAO: ...

    @abstractmethod
    async def get_user_dao(self, session: AsyncSession) -> UserDAO: ...

    @abstractmethod
    async def get_session(self) -> AsyncIterator[AsyncSession]: ...

    @abstractmethod
    async def close(self) -> None: ...

    async def __aenter__(self) -> Database:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()