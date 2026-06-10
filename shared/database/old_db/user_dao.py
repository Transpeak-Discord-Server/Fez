from typing import Optional

from shared.database.data import UserData
from shared.database.abstract_db.user_dao import UserDAO


class OldUserDAO(UserDAO):

    async def get_user(self, user_id: int) -> Optional[UserData]:
        pass

    async def get_or_create_user(self, user_id: int) -> UserData:
        pass