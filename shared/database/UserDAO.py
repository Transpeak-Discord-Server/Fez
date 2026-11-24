import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import data, tables
from shared.database.tables import User, Watchlist
from shared.utils.misc import get_week

MISSING = sentinel("MISSING")

class UserDAO:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def db_to_data_user(user: User) -> data.User:
        return data.User(user.id, user.message_count, user.under_18, user.reg_banned, user.bio, user.last_seen, user.last_message)

    async def new_user(self, user_id: int, *, message_count: int | MISSING = MISSING, under_18: bool | MISSING = MISSING, reg_banned: bool | MISSING = MISSING, bio: str | None | MISSING = MISSING, last_seen: datetime.datetime | None | MISSING = MISSING, last_message: str | None | MISSING = MISSING) -> data.User:
        existing_user = await self.get_user_info(user_id)
        if existing_user is not None: return existing_user

        if message_count is MISSING:
            message_count = 0
        if under_18 is MISSING:
            under_18 = False
        if reg_banned is MISSING:
            reg_banned = False
        if bio is MISSING:
            bio = None
        if last_seen is MISSING:
            last_seen = None
        if last_message is MISSING:
            last_message = None

        user_insert = insert(User).returning(User).values(id=user_id, message_count=message_count, under_18=under_18, reg_banned=reg_banned, bio=bio, last_seen=last_seen, last_message=last_message)
        user = (await self.session.execute(user_insert)).scalar_one()
        return self.db_to_data_user(user)

    async def update_user(self, user_id: int, *, message_count: int | MISSING = MISSING, under_18: bool | MISSING = MISSING, reg_banned: bool | MISSING = MISSING, bio: str | None | MISSING = MISSING, last_seen: datetime.datetime | None | MISSING = MISSING, last_message: str | None | MISSING = MISSING) -> data.User:
        existing_user = await self.get_user_info(user_id)
        if not existing_user:
            user = await self.new_user(user_id, message_count=message_count, under_18=under_18, reg_banned=reg_banned, bio=bio, last_seen=last_seen, last_message=last_message)
            return user

        user_update = update(User).returning(User).where(User.id == user_id)
        if message_count is not MISSING:
            user_update = user_update.values(message_count=message_count)
        if under_18 is not MISSING:
            user_update = user_update.values(under_18=under_18)
        if reg_banned is not MISSING:
            user_update = user_update.values(reg_banned=reg_banned)
        if bio is not MISSING:
            user_update = user_update.values(bio=bio)
        if last_seen is not MISSING:
            user_update = user_update.values(last_seen=last_seen)
        if last_message is not MISSING:
            user_update = user_update.values(last_message=last_message)

        db_user = (await self.session.execute(user_update)).scalar_one()
        return self.db_to_data_user(db_user)

    async def ensure_user(self, user_id: int) -> None:
        await self.new_user(user_id)

    async def get_message_count_week(self, user_id: int, week: int | None = None) -> int:
        if week is None: week = get_week()
        msg_week_select = select(tables.MessageCountWeek).where(tables.MessageCountWeek.user_id == user_id).where(
            tables.MessageCountWeek.week == week)
        result = (await self.session.execute(msg_week_select)).scalar()
        if result is None: return 0
        return result.count

    async def set_message_count_week(self, user_id: int, count: int, week: int | None = None) -> data.MessageCountWeek:
        if week is None: week = get_week()
        msg_week_insert = insert(tables.MessageCountWeek).values(user_id=user_id, week=week, count=count)
        returning_msg_week_insert = msg_week_insert.on_conflict_do_update(
            index_elements=[tables.MessageCountWeek.user_id, tables.MessageCountWeek.week],
            set_=dict(count=count)
        ).returning(tables.MessageCountWeek)
        result = (await self.session.execute(returning_msg_week_insert)).scalar_one()
        return data.MessageCountWeek(result.user_id, result.week, result.count)

    async def increment_message_count(self, user_id: int, *, step: int = 1, week: int | None = None) -> data.User:
        user = await self.get_user_info(user_id)
        if user is None:
            user = await self.new_user(user_id, message_count=step)
            await self.set_message_count_week(user_id, await self.get_message_count_week(user_id, week) + 1)
            return user

        await self.set_message_count_week(user_id, await self.get_message_count_week(user_id, week) + 1)
        return await self.set_message_count(user_id, user.message_count + step)

    async def set_message_count(self, user_id: int, count: int) -> data.User:
        return await self.update_user(user_id, message_count=count)

    async def set_user_over_18(self, user_id: int, under_18: bool) -> data.User:
        return await self.update_user(user_id, under_18=under_18)

    async def reg_ban(self, user_id: int) -> data.User:
        return await self.update_user(user_id, reg_banned=True)

    async def un_reg_ban(self, user_id: int) -> data.User:
        return await self.update_user(user_id, reg_banned=False)

    async def set_bio(self, user_id: int, bio: str | None) -> data.User:
        return await self.update_user(user_id, bio=bio)

    async def set_last_seen(self, user_id: int, last_seen: datetime.datetime | None) -> data.User:
        return await self.update_user(user_id, last_seen=last_seen)

    async def set_last_message(self, user_id: int, last_message: str | None) -> data.User:
        return await self.update_user(user_id, last_message=last_message)

    async def get_user_info(self, user_id: int) -> data.User | None:
        user_select = select(User).where(User.id == user_id)
        user = (await self.session.execute(user_select)).scalar()
        if not user: return None
        return self.db_to_data_user(user)

    async def get_watchlist(self, user_id: int) -> str | None:
        watchlist_select = select(Watchlist).where(Watchlist.user_id == user_id)
        watchlist = (await self.session.execute(watchlist_select)).scalar()
        if watchlist is None: return None
        return watchlist.description

    async def set_watchlist(self, user_id: int, watchlist: str) -> str:
        user = tables.Watchlist(user_id=user_id, description=watchlist)
        await self.session.merge(user)
        return watchlist

    async def clear_watchlist(self, user_id: int) -> bool:
        watchlist_delete = delete(Watchlist).returning(Watchlist).where(Watchlist.user_id == user_id)
        watchlist = (await self.session.execute(watchlist_delete)).scalar()
        return watchlist is not None

    async def get_special_considerations(self, user_id: int) -> str | None:
        sc_select = select(tables.SpecialConsiderations).where(tables.SpecialConsiderations.user_id == user_id)
        sc = (await self.session.execute(sc_select)).scalar()
        if not sc: return None
        return sc.description

    async def set_special_considerations(self, user_id: int, sc: str) -> str:
        sc_entry = tables.SpecialConsiderations(user_id=user_id, description=sc)
        await self.session.merge(sc_entry)
        return sc

    async def clear_special_considerations(self, user_id: int) -> bool:
        sc_delete = delete(tables.SpecialConsiderations).returning(tables.SpecialConsiderations).where(
            tables.SpecialConsiderations.user_id == user_id)
        sc = (await self.session.execute(sc_delete)).scalar()
        return sc is not None