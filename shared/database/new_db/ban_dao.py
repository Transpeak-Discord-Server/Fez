from time import time
from typing import cast

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.new_db.core import Ban

class BanDAO:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_ban(self, user_id: int) -> Ban | None:
        return cast(Ban | None, await self.session.get(Ban, user_id))

    async def ban(self, user_id: int, banned_by: int, reason: str) -> None:
        self.session.add(Ban(id=user_id, banner=banned_by, reason=reason, timestamp=int(time())))
        await self.session.commit()