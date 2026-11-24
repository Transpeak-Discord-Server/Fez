import re

import discord
from discord import app_commands
from discord.ext import commands

from shared.config import Config
from shared.database.RoleDAO import RoleDAO
from shared.database.__main__ import get_database
from shared.utils.misc import require_server
from shared.utils.permissions import permission_check, Level, has_permission

config = Config.json_config

class Roles(app_commands.Group):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.database = get_database()

        self.identity_roles: list[str] = (config['identities_for_cmd']['transfemale'] +
                                          config['identities_for_cmd']['transfemale_pronouns'] +
                                          config['identities_for_cmd']['female'] +
                                          config['identities_for_cmd']['transmale'] +
                                          config['identities_for_cmd']['transmale_pronouns'] +
                                          config['identities_for_cmd']['male'] +
                                          config['identities_for_cmd']['nonbinary'] +
                                          config['identities_for_cmd']['nonbinary_pronouns'] +
                                          config['identities_for_cmd']['cis'] +
                                          config['identities_for_cmd']['other'])
        self.other_roles: list[str] = config['cmd_can_add_roles']

        self.role_ids: list[int] = []
        for role in self.identity_roles:
            self.role_ids.append(config['rl_id'][role])
        for role in self.other_roles:
            self.role_ids.append(config['rl_id'][role])

    def get_discord_roles(self, roles: str, server: discord.Guild) -> tuple[list[discord.Role], list[str]]:
        roles_split = re.split(r'[,\s]+', roles)

        roles_to_add: list[discord.Role] = []
        could_not_add: list[str] = []

        for role_name in roles_split:
            if role_name not in self.identity_roles and role_name not in self.other_roles:
                could_not_add += role_name
                continue

            role = server.get_role(config['rl_id'].get('rl_name'))
            if role is None:
                could_not_add += role_name
                continue

            roles_to_add.append(role)

        return roles_to_add, could_not_add

    @app_commands.command()
    @app_commands.describe(roles='The roles to add, separated by spaces and/or commas.')
    @permission_check(Level.REGISTERED)
    async def add(self, interaction: discord.Interaction[commands.Bot], roles: str, user: discord.Member | None = None) -> None:
        server = await require_server(interaction)
        if server is None: return
        issuer = interaction.user
        assert isinstance(issuer, discord.Member)

        if user is not None and not has_permission(issuer, Level.HELPER):
            await interaction.response.send_message("You do not have permission to set other users' roles!")
            return

        if user is None: user = issuer

        roles_to_add, could_not_add = self.get_discord_roles(roles, server)

        await user.add_roles(*roles_to_add,
                             reason=f"/roles add_roles used by {issuer.display_name} ({issuer.id})")
        await interaction.response.send_message(
            f"Roles added to {user.display_name}.{f" Could not add: {", ".join(could_not_add)}"}")

    def get_user_roles(self, user: discord.Member) -> list[discord.Role]:
        roles: list[discord.Role] = []

        # We want these roles to be removed by /roles set too, so we treat them the same as the identity roles
        interview_role_id = config['rl_id']['interview']
        readrules_role_id = config['rl_id']['readrules']

        for role in user.roles:
            if role.id not in self.role_ids and role.id not in [interview_role_id, readrules_role_id]:
                continue
            roles.append(role)

        return roles

    @app_commands.command()
    @app_commands.describe(roles='The roles to remove, separated by spaces and/or commas.')
    @permission_check(Level.REGISTERED)
    async def remove(self, interaction: discord.Interaction[commands.Bot], roles: str, user: discord.Member | None = None) -> None:
        server = await require_server(interaction)
        if server is None: return
        issuer = interaction.user
        assert isinstance(issuer, discord.Member)

        if user is not None and not has_permission(issuer, Level.HELPER):
            await interaction.response.send_message("You do not have permission to set other users' roles!")
            return

        if user is None: user = issuer

        roles_to_remove, could_not_find = self.get_discord_roles(roles, server)

        await user.remove_roles(*roles_to_remove, reason=f"/roles remove used by {issuer.display_name} ({issuer.id})")
        await interaction.response.send_message(f"Roles removed from {user.display_name}.{f"Could not add: {", ".join(could_not_find)}"}")

    @app_commands.command()
    @app_commands.describe(roles='The roles to set, separated by spaces and/or commas.')
    @permission_check(Level.STAFF)
    async def set(self, interaction: discord.Interaction[commands.Bot], roles: str, user: discord.Member | None = None) -> None:
        server = await require_server(interaction)
        if server is None: return
        issuer = interaction.user
        assert isinstance(issuer, discord.Member)

        if user is None: user = issuer

        user_roles = self.get_user_roles(user)
        await user.remove_roles(*user_roles, reason=f"/roles set used by {issuer.display_name} ({issuer.id})")

        roles_to_add, could_not_add = self.get_discord_roles(roles, server)

        await user.add_roles(*roles_to_add,
                             reason=f"/roles add_roles used by {issuer.display_name} ({issuer.id})")
        await interaction.response.send_message(
            f"Roles added to {user.display_name}.{f" Could not add: {", ".join(could_not_add)}"}")

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def saved(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member | None) -> None:
        server = await require_server(interaction)
        if server is None: return

        issuer = interaction.user
        assert isinstance(issuer, discord.Member)
        if user is None: user = issuer

        async with self.database.get_session() as session:
            role_dao = RoleDAO(session)
            roles = await role_dao.get_saved_roles(user.id, server)

        if len(roles) == 0:
            await interaction.response.send_message(f"Could not find any saved roles for user {user.display_name}")
            return

        await interaction.response.send_message(f"**{user.display_name}'s saved roles:**\n"
                                                f"{", ".join([role.name for role in roles])}")