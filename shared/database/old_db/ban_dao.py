from shared.database.abstract_db.ban_dao import BanDAO
from shared.database.data import BanData


class OldBanDAO(BanDAO):

    async def get_bans(self, user_id: int) -> list[BanData]:
        pass

    async def add_ban(self, user_id: int, banner_id: int, timestamp: int, reason: str) -> BanData:
        pass