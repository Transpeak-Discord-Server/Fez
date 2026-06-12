from datetime import datetime

from sqlalchemy import select

from shared.database.abstract_db.msgcount_dao import MsgCountDAO
from shared.database.old_db.tables import _Msgcount, _MsgcountWeek


def get_week() -> int:
    a = datetime(2017, 7, 31, 00, 00, 00)
    b = datetime.now()
    return int((b - a).total_seconds() / (7 * 24 * 60 * 60))

class OldMsgCountDAO(MsgCountDAO):

    async def increment_message_count(self, user_id: int, msg:str, amount: int = 1) -> None:
        user_select = select(_Msgcount).where(_Msgcount.id == str(user_id))
        user = (await self.session.scalars(user_select)).first()
        if user is None:
            user = _Msgcount(id=str(user_id), count="0", lastmsg=msg)
            self.session.add(user)
        curr_count = int(user.count)
        user.count = str(curr_count + amount)
        user.lastmsg = msg
        await self.session.commit()
        await self.increment_weekly_count(user_id, get_week(), amount)
        return None

    async def increment_weekly_count(self, user_id: int, week: int, amount: int = 1) -> None:
        user_select = select(_MsgcountWeek).where(_MsgcountWeek.id == str(user_id) and _MsgcountWeek.week == str(week))
        user = (await self.session.scalars(user_select)).first()
        if user is None:
            user = _MsgcountWeek(id=str(user_id), week=str(week), count="0")
        curr_count = int(user.count)
        user.count = str(curr_count + amount)
        await self.session.commit()
        return None

    async def get_week_messages(self, user_id: int, week: int) -> int:
        user_select = select(_MsgcountWeek).where(_MsgcountWeek.id == str(user_id) and _MsgcountWeek.week == str(week))
        user = (await self.session.scalars(user_select)).first()
        if user is None:
            return 0
        return int(user.count)

    async def get_message_count(self, user_id: int) -> int:
        user_select = select(_Msgcount).where(_Msgcount.id == str(user_id))
        user = (await self.session.scalars(user_select)).first()
        if user is None:
            return 0
        return int(user.count)