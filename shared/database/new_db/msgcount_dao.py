from datetime import datetime
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.new_db.core import User, UserMessagesWeek


def get_week() -> int:
    a = datetime(2017, 7, 31, 00, 00, 00)
    b = datetime.now()
    return int((b - a).total_seconds() / (7 * 24 * 60 * 60))

class MsgCountDAO:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_msg_count(self, user_id: int) -> int:
        user: User | None = cast(User | None, await self.session.get(User, user_id))
        if user:
            return user.message_count
        return 0

    async def get_msg_count_week(self, user_id: int, week: int) -> int:
        user_messages: UserMessagesWeek | None = cast(UserMessagesWeek | None, await self.session.get(UserMessagesWeek, (user_id, week)))
        if user_messages:
            return user_messages.messages
        return 0

    async def increment_msg_count(self, user_id: int) -> None:
        user = await self.session.get(User, user_id)
        if not user:
            return None
        user.message_count += 1

        current_week = get_week()
        user_week = await self.session.get(UserMessagesWeek, (user_id, current_week))
        if user_week:
            user_week.messages += 1
        else:
            user_week = UserMessagesWeek(id=user_id, messages=1, week=current_week)
            self.session.add(user_week)

        await self.session.commit()
        return None