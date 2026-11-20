import datetime

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import data
from shared.database.tables import User


class UserDAO:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def new_user(self, user_id: int, *, message_count: int = 0, under_18: bool = False, reg_banned: bool = False, bio: str | None = None, last_seen: datetime.datetime | None = None, last_message: str | None = None) -> data.User:
        user_insert = insert(User).returning(User).values(id=user_id, message_count=message_count, under_18=under_18, reg_banned=reg_banned, bio=bio, last_seen=last_seen, last_message=last_message)
        user = (await self.session.execute(user_insert)).scalar_one()
        return data.User(user.id, user.message_count, user.under_18, user.reg_banned, user.bio, user.last_seen, user.last_message)

    async def get_user_info(self, user_id: int) -> data.User | None:
        user_select = select(User).where(User.id == user_id)
        user = (await self.session.execute(user_select)).scalar()
        if not user: return None
        return data.User(user_id, user.message_count, user.under_18, user.reg_banned, user.bio, user.last_seen, user.last_message)