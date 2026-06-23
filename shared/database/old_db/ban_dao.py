from sqlalchemy import select
from shared.database.abstract_db.ban_dao import BanDAO
from shared.database.data import BanData
from shared.database.old_db.tables import _Ban, _Banlink


class OldBanDAO(BanDAO):

    async def remove_ban(self, user_id: int, timestamp: int) -> bool:
        ban_select = select(_Ban).where(_Ban.userid == str(user_id)).where(_Ban.timestamp == str(timestamp))
        ban = (await self.session.scalars(ban_select)).first()
        if ban is None:
            return False
        await self.session.delete(ban)
        await self.session.commit()
        return True

    async def get_bans(self, user_id: int) -> list[BanData]:
        bans_select = select(_Ban).where(_Ban.userid == str(user_id))
        bans = (await self.session.scalars(bans_select)).all()
        if not bans:
            return []
        bans_with_links: list[BanData] = []
        for ban in bans:
            links_select = select(_Banlink).where(_Banlink.userid == ban.userid).where(_Banlink.timestamp == ban.timestamp)
            links = (await self.session.scalars(links_select)).all()
            bans_with_links.append(BanData(int(ban.userid), int(ban.banner), int(ban.timestamp), str(ban.reason), [
                str(x.link) for x in links
            ]))
        return bans_with_links

    async def add_ban(self, user_id: int, banner_id: int, timestamp: int, reason: str, links: list[str]) -> BanData:
        ban = _Ban(userid=str(user_id), banner=str(banner_id), timestamp=str(timestamp), reason=reason)
        self.session.add(ban)
        for link in links:
            ban_link = _Banlink(userid=str(user_id), timestamp=str(timestamp), link=link)
            self.session.add(ban_link)
        await self.session.commit()
        return BanData(user_id, banner_id, timestamp, reason, links)