from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.core import UserRoles


class RoleDAO:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_roles(self, user_id: int) -> Sequence[int]:
        return (await self.session.execute(select(UserRoles.role)
                    .where(UserRoles.id == user_id))).scalars().all()

    async def set_roles(self, user_id: int, roles: list[int]) -> None:
        await self.session.execute(delete(UserRoles).where(UserRoles.id == user_id))

        for role in roles:
            self.session.add(UserRoles(id=user_id, role=role))

        await self.session.commit()