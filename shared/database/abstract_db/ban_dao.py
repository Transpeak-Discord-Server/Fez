from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.data import BanData


class BanDAO(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def remove_ban(self, user_id: int, timestamp: int) -> bool: ...

    @abstractmethod
    async def add_ban(self, user_id: int, banner_id: int, timestamp: int, reason: str, links: list[str]) -> BanData: ...

    @abstractmethod
    async def get_bans(self, user_id: int) -> list[BanData]: ...