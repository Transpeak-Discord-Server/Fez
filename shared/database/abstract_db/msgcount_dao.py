from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

class MsgCountDAO(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def increment_message_count(self, user_id: int, amount: int = 1) -> None: ...

    @abstractmethod
    async def increment_weekly_count(self, user_id: int, week: int, amount: int = 1) -> None: ...

    @abstractmethod
    async def get_week_messages(self, user_id: int, week: int) -> int: ...

    @abstractmethod
    async def get_message_count(self, user_id: int) -> int: ...