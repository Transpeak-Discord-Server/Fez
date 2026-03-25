from shared.database.core import Database


class RolesManager:

    def __init__(self):
        self.db = Database("roles.db")

    async def get_roles(self, user_id: int):
        async with self.db.connection as conn:
            roles = await conn.fetchone("SELECT roles FROM roles WHERE userid = ?", (str(user_id),))
        return roles

    async def set_roles(self, user_id: int, roles: list[int]):
        async with self.db.connection as conn:
            await conn.execute("INSERT OR REPLACE INTO roles (userid, roles) VALUES (?, ?)", (str(user_id), roles))