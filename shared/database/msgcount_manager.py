from datetime import datetime
from core import Database

class MsgCountManager:

    def __init__(self):
        self.msgcount_db = Database("message_count.db")
        self.msgcount_week_db = Database("message_count_week.db")

    @staticmethod
    def getweek() -> str:
        a = datetime(2017, 7, 31, 00, 00, 00)
        b = datetime.now()
        return str(int((b - a).total_seconds() / (7 * 24 * 60 * 60)))

    async def get_msg_count(self, user_id: int, week: bool = False) -> int:
        if week:
            db = self.msgcount_week_db
            query = "SELECT count FROM msgcount_week WHERE id = ? and week = ?"
            args = (str(user_id),self.getweek())
        else:
            db = self.msgcount_db
            query = "SELECT count FROM msgcount WHERE id = ?"
            args = (str(user_id),)
        async with db.connection as conn:
            row = await conn.fetchone(query, *args)
        return row['count'] if row else 0

    async def increment_msg_count(self, user_id: int):
        week = self.getweek()
        user = str(user_id)
        async with self.msgcount_db.connection as conn:
            await conn.execute(
                "INSERT INTO msgcount (id, count) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET count = count + 1",
                (user, 1)
            )

        async with self.msgcount_week_db.connection as conn:
            await conn.execute(
            "INSERT INTO msgcount_week (id, count, week) VALUES (?, ?, ?) ON CONFLICT(id, week) DO UPDATE SET count = count + 1",
            (user, 1, week)
            )

    async def set_msg_count(self, user_id: int, count: int):
        async with self.msgcount_db.connection as conn:
            await conn.execute(
                "INSERT INTO msgcount (id, count) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET count = ?",
                (str(user_id), count, count)
            )
        async with self.msgcount_week_db.connection as conn:
            await conn.execute(
            "INSERT INTO msgcount_week (id, count) VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET count = ?",
            (str(user_id), count, count)
            )

