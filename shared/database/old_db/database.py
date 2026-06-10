import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from shared.database.abstract_db.ban_dao import BanDAO
from shared.database.abstract_db.database import Database
from shared.database.abstract_db.msgcount_dao import MsgCountDAO
from shared.database.abstract_db.role_dao import RoleDAO
from shared.database.abstract_db.user_dao import UserDAO
from shared.database.old_db.ban_dao import OldBanDAO
from shared.database.old_db.msgcount_dao import OldMsgCountDAO
from shared.database.old_db.role_dao import OldRoleDAO
from shared.database.old_db.user_dao import OldUserDAO


class OldDatabase(Database):

    async def get_ban_dao(self, session: AsyncSession) -> BanDAO:
        return OldBanDAO(session)

    async def get_msgcount_dao(self, session: AsyncSession) -> MsgCountDAO:
        return OldMsgCountDAO(session)

    async def get_role_dao(self, session: AsyncSession) -> RoleDAO:
        return OldRoleDAO(session)

    async def get_user_dao(self, session: AsyncSession) -> UserDAO:
        return OldUserDAO(session)

    _engine = create_async_engine(os.environ["DATABASE_INFO"], echo=True)
    async_session = async_sessionmaker(bind=_engine, expire_on_commit=False)

    async def close(self) -> None:
        pass # TODO

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.async_session() as session:
            try:
                yield session
            finally:
                await session.close()