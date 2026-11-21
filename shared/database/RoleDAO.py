import discord
from sqlalchemy import select, Insert, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

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

        # TODO: When UserDAO is merged into main, add a thing here to make sure the user exists in the user table

        statements: list[Insert] = []
        for role in roles:
            statement = insert(UserRole).values(user_id=user_id, role_id=role)
            statements.append(statement)
        self.session.add_all(statements)

    async def save_roles(self, user_id: int, roles: list[discord.Role]) -> None:
        role_ids: list[int] = []

        for role in roles:
            role_ids.append(role.id)

        await self.save_role_ids(user_id, role_ids)