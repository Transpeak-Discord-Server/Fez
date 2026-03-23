from shared.database.core import Database


class RolesManager:

    def __init__(self):
        self.db = Database("roles.db")

    async def initialise(self):
        await self.db.connect()

    def get_roles(self, user_id: int):
        roles = self.db.fetchone("SELECT roles FROM roles WHERE userid = ?", (str(user_id),))
        return roles

    def set_roles(self, user_id: int, roles: list[int]):
        self.db.execute("INSERT OR REPLACE INTO roles (userid, roles) VALUES (?, ?)", (str(user_id), roles))