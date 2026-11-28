# Fez/TransBot - A Discord.py bot for Transpeak
# Copyright (C) 2026 Fez project contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from shared.database import data, tables
from shared.database.UserDAO import UserDAO
from shared.utils.misc import get_week


class MessageCountDAO:

    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_top_10(self) -> list[data.User]:
        user_select = select(tables.User).order_by(desc(tables.User.message_count)).limit(10)
        result = (await self.session.execute(user_select)).scalars()
        return [UserDAO.db_to_data_user(user) for user in result]

    async def get_top_10_week(self) -> list[data.MessageCountWeek]:
        user_select = select(tables.MessageCountWeek).where(tables.MessageCountWeek.week==get_week()).order_by(desc(tables.MessageCountWeek.count)).limit(10)
        result = (await self.session.execute(user_select)).scalars()
        return [data.MessageCountWeek(user.user_id, user.week, user.count) for user in result]