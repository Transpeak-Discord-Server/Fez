from abc import ABC, abstractmethod
from typing import Optional, Any

from shared.database.data import UserData, BanData


class AbstractDatabase(ABC):

    @abstractmethod
    async def close(self) -> None: ...

    async def __aenter__(self) -> AbstractDatabase:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()