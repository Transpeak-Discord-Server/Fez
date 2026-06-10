from abc import ABC, abstractmethod

from shared.database.data import BanData


class BanDAO(ABC):

    @abstractmethod
    async def add_ban(self, user_id: int, banner_id: int, timestamp: int, reason: str) -> BanData: ...

    @abstractmethod
    async def get_bans(self, user_id: int) -> list[BanData]: ...