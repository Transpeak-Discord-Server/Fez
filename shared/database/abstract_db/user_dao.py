from abc import ABC, abstractmethod
from typing import Optional

from shared.database.data import UserData


class UserDAO(ABC):

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[UserData]: ...

    @abstractmethod
    async def get_or_create_user(self, user_id: int) -> UserData: ...