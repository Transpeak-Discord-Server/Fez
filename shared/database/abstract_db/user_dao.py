from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from shared.database.data import UserData


class UserDAO(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_user(self, user_id: int) -> Optional[UserData]: ...

    @abstractmethod
    async def get_or_create_user(self, user_id: int) -> UserData: ...