from datetime import datetime, timezone
from typing import Any

from sqlalchemy import insert, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import data, tables
from shared.database.UserDAO import UserDAO
from shared.database.data import BanType
from shared.database.tables import Ban

class BanDAO:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_ban(self, user_id: int, reason: str, issuer_id: int, ban_type: BanType, timestamp: datetime | None = None) -> data.Ban:
        if timestamp is None:
            timestamp = datetime.now(tz=timezone.utc)

        if not await UserDAO(self.session).get_user_info(user_id):
            await UserDAO(self.session).new_user(user_id)

        if not await UserDAO(self.session).get_user_info(issuer_id):
            await UserDAO(self.session).new_user(issuer_id)

        ban_statement = insert(Ban).returning(Ban).values(user_id=user_id, reason=reason, issuer_id=issuer_id, ban_timestamp=timestamp, ban_type=ban_type.value)
        ban = (await self.session.execute(ban_statement)).scalar_one()
        await self.session.commit()

        return data.Ban(ban.ban_id, user_id, issuer_id, reason, timestamp, ban_type)

    data_to_db_enum = {
        data.BanType.Permanent: tables.BanType.permanent,
        data.BanType.Temporary: tables.BanType.temporary,
        data.BanType.VC: tables.BanType.vc,
        data.BanType.VCSoft: tables.BanType.vc_soft
    }

    db_to_data_enum = {
        tables.BanType.permanent: data.BanType.Permanent,
        tables.BanType.temporary: data.BanType.Temporary,
        tables.BanType.vc: data.BanType.VC,
        tables.BanType.vc_soft: data.BanType.VCSoft
    }

    async def edit_ban(self, ban_id: int, *, reason: str | None = None, ban_type: BanType | None = None, timestamp: datetime | None = None) -> data.Ban:
        values: dict[str, Any] = {}
        if ban_type is not None:
            values["ban_type"] = self.data_to_db_enum[ban_type]
        if timestamp is not None:
            values["ban_timestamp"] = timestamp
        if reason is not None:
            values["reason"] = reason

        if not values: raise ValueError("Nothing to update")

        ban_update = update(Ban).returning(Ban).where(Ban.ban_id == ban_id).values(**values)
        ban = (await self.session.execute(ban_update)).scalar()
        if not ban: raise ValueError("Ban not found.")

        await self.session.commit()
        return data.Ban(ban.ban_id, ban.user_id, ban.issuer_id, ban.reason, ban.ban_timestamp, self.db_to_data_enum[ban.ban_type])

    async def get_ban(self, ban_id: int) -> data.Ban | None:
        ban_select_statement = select(Ban).where(Ban.ban_id == ban_id)
        ban = (await self.session.execute(ban_select_statement)).scalar()
        if ban is None: return None
        return data.Ban(ban.ban_id, ban.user_id, ban.issuer_id, ban.reason, ban.ban_timestamp, self.db_to_data_enum[ban.ban_type])

    async def get_bans(self, user_id: int) -> list[data.Ban]:
        ban_select_statement = select(Ban).where(Ban.user_id == user_id)
        db_bans = (await self.session.execute(ban_select_statement)).scalars().all()
        bans: list[data.Ban] = []
        for db_ban in db_bans:
            ban = data.Ban(db_ban.ban_id, db_ban.user_id, db_ban.issuer_id, db_ban.reason, db_ban.ban_timestamp, self.db_to_data_enum[db_ban.ban_type])
            bans.append(ban)
        return bans

    async def remove_ban(self, ban_id: int) -> None:
        del_statement = delete(Ban).where(Ban.ban_id == ban_id)
        await self.session.execute(del_statement)
        await self.session.commit()