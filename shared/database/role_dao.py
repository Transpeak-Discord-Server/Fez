from abc import ABC, abstractmethod

class RoleDAO(ABC):

    @abstractmethod
    async def get_user_roles(self, user_id: int) -> list[int]: ...

    @abstractmethod
    async def set_user_roles(self, user_id: int, roles: list[int]) -> None: ...

    @abstractmethod
    async def add_user_role(self, user_id: int, role: int) -> None: ...

    @abstractmethod
    async def remove_user_role(self, user_id: int, role: int) -> None: ...