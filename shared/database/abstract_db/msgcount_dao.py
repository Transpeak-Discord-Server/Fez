from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.data import UserMessagesWeekData


class MsgCountDAO(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def set_message_count(self, user_id: int, amount: int) -> None: ...

    @abstractmethod
    async def set_week_count(self, user_id: int, week: int, amount: int) -> None: ...

    @abstractmethod
    async def increment_message_count(self, user_id: int, msg: str, amount: int = 1) -> None: ...

    @abstractmethod
    async def increment_weekly_count(self, user_id: int, week: int, amount: int = 1) -> None: ...

    @abstractmethod
    async def get_week_messages(self, user_id: int, week: int) -> int: ...

    @abstractmethod
    async def get_all_week_messages(self, user_id: int) -> list[UserMessagesWeekData]: ...

    @abstractmethod
    async def get_message_count(self, user_id: int) -> int: ...