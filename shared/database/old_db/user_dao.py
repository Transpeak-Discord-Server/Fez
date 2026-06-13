from typing import Optional

from shared.database.data import UserData
from shared.database.abstract_db.user_dao import UserDAO
from shared.database.old_db.ban_dao import OldBanDAO
from shared.database.old_db.msgcount_dao import OldMsgCountDAO
from shared.database.old_db.role_dao import OldRoleDAO
from shared.utils.misc import get_week


class OldUserDAO(UserDAO):

    async def get_user(self, user_id: int) -> Optional[UserData]:
        message_count = await OldMsgCountDAO(self.session).get_message_count(user_id)
        roles = await OldRoleDAO(self.session).get_user_roles(user_id)
        bans = await OldBanDAO(self.session).get_bans(user_id)
        weekly_messages = await OldMsgCountDAO(self.session).get_all_week_messages(user_id)
        if message_count is None or roles is None or bans is None or weekly_messages is None:
            return None
        return UserData(user_id, message_count, roles, bans, weekly_messages)

    async def get_or_create_user(self, user_id: int) -> UserData:
        message_count = await OldMsgCountDAO(self.session).get_message_count(user_id)
        if not message_count:
            await OldMsgCountDAO(self.session).set_message_count(user_id, 0)
        roles = await OldRoleDAO(self.session).get_user_roles(user_id)
        if not roles:
            await OldRoleDAO(self.session).set_user_roles(user_id, [])
        bans = await OldBanDAO(self.session).get_bans(user_id)
        weekly_messages = await OldMsgCountDAO(self.session).get_all_week_messages(user_id)
        if not weekly_messages:
            await OldMsgCountDAO(self.session).set_week_count(user_id, get_week(), 0)
        return UserData(user_id, message_count, roles, bans, weekly_messages)