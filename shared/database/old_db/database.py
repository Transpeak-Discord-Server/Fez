import os

from sqlalchemy.ext.asyncio import AsyncSession

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

    def __init__(self) -> None:
        super().__init__(os.environ["DATABASE_INFO"])

    def ban_dao(self, session: AsyncSession) -> BanDAO:
        return OldBanDAO(session)

    def msgcount_dao(self, session: AsyncSession) -> MsgCountDAO:
        return OldMsgCountDAO(session)

    def role_dao(self, session: AsyncSession) -> RoleDAO:
        return OldRoleDAO(session)

    def user_dao(self, session: AsyncSession) -> UserDAO:
        return OldUserDAO(session)