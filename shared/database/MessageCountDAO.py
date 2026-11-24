from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import data, tables
from shared.database.UserDAO import UserDAO
from shared.utils.misc import get_week


class MessageCountDAO:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_top_10(self) -> list[data.User]:
        user_select = select(tables.User).order_by(desc(tables.User.message_count)).limit(10)
        result = (await self.session.execute(user_select)).scalars()
        return [UserDAO.db_to_data_user(user) for user in result]

    async def get_top_10_week(self) -> list[data.MessageCountWeek]:
        user_select = select(tables.MessageCountWeek).where(tables.MessageCountWeek.week==get_week()).order_by(desc(tables.MessageCountWeek.count)).limit(10)
        result = (await self.session.execute(user_select)).scalars()
        return [data.MessageCountWeek(user.user_id, user.week, user.count) for user in result]