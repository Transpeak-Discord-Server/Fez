from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import data
from shared.database.tables import User


class UserDAO:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_info(self, user_id: int) -> data.User | None:
        user_select = select(User).where(User.id == user_id)
        user = (await self.session.execute(user_select)).scalar()
        if not user: return None
        return data.User(user_id, user.message_count, user.under_18, user.reg_banned, user.bio, user.last_seen, user.last_message)