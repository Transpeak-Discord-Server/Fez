from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class RoleDAO(ABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def get_user_roles(self, user_id: int) -> list[int]: ...

    @abstractmethod
    async def set_user_roles(self, user_id: int, roles: list[int]) -> None: ...