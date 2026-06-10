from abc import ABC, abstractmethod
from typing import Optional, Any

from shared.database.data import UserData, BanData


class AbstractDatabase(ABC):

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[UserData]: ...

    @abstractmethod
    async def get_or_create_user(self, user_id: int) -> UserData: ...

    @abstractmethod
    async def increment_message_count(self, user_id: int, amount: int = 1) -> None: ...

    @abstractmethod
    async def increment_weekly_count(self, user_id: int, week: int, amount: int = 1) -> None: ...

    @abstractmethod
    async def get_week_messages(self, user_id: int, week: int) -> int: ...

    @abstractmethod
    async def add_ban(self, user_id: int, banner_id: int, timestamp: int, reason: str) -> BanData: ...

    @abstractmethod
    async def get_bans(self, user_id: int) -> list[BanData]: ...

    @abstractmethod
    async def get_user_roles(self, user_id: int) -> list[int]: ...

    @abstractmethod
    async def set_user_roles(self, user_id: int, roles: list[int]) -> None: ...

    @abstractmethod
    async def add_user_role(self, user_id: int, role: int) -> None: ...

    @abstractmethod
    async def remove_user_role(self, user_id: int, role: int) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...

    async def __aenter__(self) -> AbstractDatabase:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()