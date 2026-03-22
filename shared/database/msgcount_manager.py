from core import Database

class MsgCountManager:

    def __init__(self):
        self.msgcount_db = Database("message_count.db")
        self.msgcount_week_db = Database("message_count_week.db")

    async def get_msg_count(self, user_id: int, week: bool = False) -> int:
        if week:
            cursor = await self.msgcount_week_db.execute("SELECT count FROM msgcount_week WHERE id = ?", (str(user_id),))
            return cursor.fetchone()[0]
        cursor = await self.msgcount_db.execute("SELECT count FROM msgcount WHERE id = ?", (str(user_id),))
        return cursor.fetchone()[0]

    async def increment_msg_count(self, user_id: int):
        await self.msgcount_db.execute("UPDATE msgcount SET count = count + 1 WHERE id = ?", (str(user_id),))
        await self.msgcount_db.commit()
        await self.msgcount_week_db.execute("UPDATE msgcount_week SET count = count + 1 WHERE id = ?", (str(user_id),))
        await self.msgcount_week_db.commit()
