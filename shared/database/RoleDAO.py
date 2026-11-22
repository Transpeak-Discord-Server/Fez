import discord
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.UserDAO import UserDAO
from shared.database.tables import UserRole


class RoleDAO:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_saved_role_ids(self, user_id: int) -> list[int]:
        role_select = select(UserRole).where(UserRole.user_id == user_id)
        role_ids = (await self.session.execute(role_select)).scalars().all()

        ids: list[int] = []
        for role in role_ids:
            ids.append(role.role_id)

        return ids

    async def get_saved_roles(self, user_id: int, server: discord.Guild) -> list[discord.Role]:
        role_ids = await self.get_saved_role_ids(user_id)

        roles: list[discord.Role] = []

        for role_id in role_ids:
            role = server.get_role(role_id)
            if not role:
                print(f"could not find role with ID: {role_id}")
                continue
            roles.append(role)

        return roles

    async def clear_saved_roles(self, user_id: int) -> None:
        statement = delete(UserRole).where(UserRole.user_id == user_id)
        await self.session.execute(statement)

    async def save_role_ids(self, user_id: int, roles: list[int]) -> None:
        await self.clear_saved_roles(user_id)

        await UserDAO(self.session).ensure_user(user_id)

        db_objects: list[UserRole] = []
        for role in roles:
            user_role = UserRole(user_id=user_id, role_id=role)
            db_objects.append(user_role)
        self.session.add_all(db_objects)

    async def save_roles(self, user_id: int, roles: list[discord.Role]) -> None:
        role_ids: list[int] = []

        for role in roles:
            role_ids.append(role.id)

        await self.save_role_ids(user_id, role_ids)