from sqlalchemy import select
from shared.database.abstract_db.ban_dao import BanDAO
from shared.database.data import BanData
from shared.database.old_db.tables import _Ban


class OldBanDAO(BanDAO):

    async def get_bans(self, user_id: int) -> list[BanData]:
        bans_select = select(_Ban).where(_Ban.userid == str(user_id))
        bans = (await self.session.scalars(bans_select)).all()
        if not bans:
            return []
        return [
            BanData(int(ban.userid), int(ban.banner), int(ban.timestamp), str(ban.reason))
            for ban in bans
        ]

    async def add_ban(self, user_id: int, banner_id: int, timestamp: int, reason: str) -> BanData:
        ban = _Ban(userid=str(user_id), banner=str(banner_id), timestamp=str(timestamp), reason=reason)
        self.session.add(ban)
        await self.session.commit()
        return BanData(user_id, banner_id, timestamp, reason)