from shared.database.abstract_db.role_dao import RoleDAO


class OldRoleDAO(RoleDAO):

    async def get_user_roles(self, user_id: int) -> list[int]:
        pass

    async def set_user_roles(self, user_id: int, roles: list[int]) -> None:
        pass

    async def add_user_role(self, user_id: int, role: int) -> None:
        pass

    async def remove_user_role(self, user_id: int, role: int) -> None:
        pass