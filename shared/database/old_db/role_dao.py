from shared.database.abstract_db.role_dao import RoleDAO
from shared.database.old_db.tables import _Role


class OldRoleDAO(RoleDAO):

    async def get_user_roles(self, user_id: int) -> list[int]:
        roles_result = await self.session.get(_Role, str(user_id))
        if roles_result is None:
            return []
        roles: list[int] = []
        for x in roles_result.roles.split(','):
            roles.append(int(x))
        return roles

    async def set_user_roles(self, user_id: int, roles: list[int]) -> None:
        roles_str = ""
        for x, role in enumerate(roles):
            roles_str += str(role) + ("," if x == len(roles) - 1 else "")

        user = await self.session.get(_Role, str(user_id))
        if user is None:
            user = _Role(userid=str(user_id), roles="")
        user.roles = roles_str
        await self.session.commit()