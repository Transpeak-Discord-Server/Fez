from shared.database.abstract_db.msgcount_dao import MsgCountDAO


class OldMsgCountDAO(MsgCountDAO):

    async def increment_message_count(self, user_id: int, amount: int = 1) -> None:
        pass

    async def increment_weekly_count(self, user_id: int, week: int, amount: int = 1) -> None:
        pass

    async def get_week_messages(self, user_id: int, week: int) -> int:
        pass

    async def get_message_count(self, user_id: int) -> int:
        pass