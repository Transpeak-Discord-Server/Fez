from time import time
from typing import Any

from core import Database

class BanManager:

    def __init__(self):
        self.ban_db = Database("bans.db")

    async def get_ban(self, user_id: int) -> dict[str, Any]:
        async with self.ban_db.connection as conn:
            row = await conn.fetchone("SELECT * FROM bans WHERE userid = ?", (str(user_id),))
        return {
            "userid": row['userid'],
            "banned_by": row['banner'],
            "timestamp": row['timestamp'],
            "reason": row['reason']
        }

    async def ban(self, user_id: int, banned_by: int, reason: str):
        async with self.ban_db.connection as conn:
            await conn.execute(
                "INSERT INTO bans (userid, banner, timestamp, reason) VALUES (?, ?, ?, ?)",
                (str(user_id), str(banned_by), int(round(time() * 1000)), reason)
            )