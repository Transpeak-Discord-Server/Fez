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

import re

import discord
from discord import app_commands

from shared.database.RoleDAO import RoleDAO
from shared.database.UserDAO import UserDAO
from shared.transpeak_bot import TranspeakBot
from shared.utils.misc import require_server
from shared.utils.permissions import permission_check, Level, has_permission

class Roles(app_commands.Group):

    def __init__(self, bot: TranspeakBot):
        super().__init__()
        self.bot = bot

        self.identity_roles: list[str] = (self.bot.config['identities_for_cmd']['transfemale'] +
                                          self.bot.config['identities_for_cmd']['transfemale_pronouns'] +
                                          self.bot.config['identities_for_cmd']['female'] +
                                          self.bot.config['identities_for_cmd']['transmale'] +
                                          self.bot.config['identities_for_cmd']['transmale_pronouns'] +
                                          self.bot.config['identities_for_cmd']['male'] +
                                          self.bot.config['identities_for_cmd']['nonbinary'] +
                                          self.bot.config['identities_for_cmd']['nonbinary_pronouns'] +
                                          self.bot.config['identities_for_cmd']['cis'] +
                                          self.bot.config['identities_for_cmd']['other'])
        self.other_roles: list[str] = self.bot.config['cmd_can_add_roles']

        self.role_ids: list[int] = []
        for role in self.identity_roles:
            self.role_ids.append(self.bot.config['rl_id'][role])
        for role in self.other_roles:
            self.role_ids.append(self.bot.config['rl_id'][role])

    def get_discord_roles(self, roles: str, server: discord.Guild) -> tuple[list[discord.Role], list[str]]:
        roles_split = re.split(r'[,\s]+', roles)

        roles_to_add: list[discord.Role] = []
        could_not_add: list[str] = []

        for role_name in roles_split:
            if role_name not in self.identity_roles and role_name not in self.other_roles:
                could_not_add.append(role_name)
                continue

            role = server.get_role(self.bot.config['rl_id'].get(role_name))
            if role is None:
                could_not_add.append(role_name)
                continue

            roles_to_add.append(role)

        return roles_to_add, could_not_add

    @app_commands.command()
    @app_commands.describe(roles='The roles to add, separated by spaces and/or commas.')
    @permission_check(Level.REGISTERED)
    async def add(self, interaction: discord.Interaction[TranspeakBot], roles: str, user: discord.Member | None = None) -> None:
        server = await require_server(interaction)
        if server is None: return

        await interaction.response.defer(thinking=True)

        issuer = interaction.user
        assert isinstance(issuer, discord.Member)

        if user is not None and not has_permission(issuer, Level.HELPER):
            await interaction.followup.send("You do not have permission to set other users' roles!")
            return

        if user is None: user = issuer

        roles_to_add, could_not_add = self.get_discord_roles(roles, server)

        await user.add_roles(*roles_to_add,
                             reason=f"/roles add_roles used by {issuer.display_name} ({issuer.id})")
        await interaction.followup.send(
            f"Roles added to {user.display_name}.{f" Could not add: {", ".join(could_not_add)}"  if len(could_not_add) != 0 else ""}")

    def get_user_roles(self, user: discord.Member) -> list[discord.Role]:
        roles: list[discord.Role] = []

        # We want these roles to be removed by /roles set too, so we treat them the same as the identity roles
        interview_role_id = self.bot.config['rl_id']['interview']
        readrules_role_id = self.bot.config['rl_id']['readrules']
        regular_role_id = self.bot.config['rl_id']['regular']
        new_role_id = self.bot.config['rl_id']['new']

        for role in user.roles:
            if role.id not in self.role_ids and role.id not in [interview_role_id, readrules_role_id, regular_role_id, new_role_id]:
                continue
            roles.append(role)

        return roles

    @app_commands.command()
    @app_commands.describe(roles='The roles to remove, separated by spaces and/or commas.')
    @permission_check(Level.REGISTERED)
    async def remove(self, interaction: discord.Interaction[TranspeakBot], roles: str, user: discord.Member | None = None) -> None:
        server = await require_server(interaction)
        if server is None: return

        await interaction.response.defer(thinking=True)

        issuer = interaction.user
        assert isinstance(issuer, discord.Member)

        if user is not None and not has_permission(issuer, Level.HELPER):
            await interaction.followup.send("You do not have permission to set other users' roles!")
            return

        if user is None: user = issuer

        roles_to_remove, could_not_find = self.get_discord_roles(roles, server)

        await user.remove_roles(*roles_to_remove, reason=f"/roles remove used by {issuer.display_name} ({issuer.id})")
        await interaction.followup.send(f"Roles removed from {user.display_name}.{f"Could not add: {", ".join(could_not_find)}"  if len(could_not_find) != 0 else ""}")

    @app_commands.command()
    @app_commands.describe(roles='The roles to set, separated by spaces and/or commas.')
    @permission_check(Level.STAFF)
    async def set(self, interaction: discord.Interaction[TranspeakBot], roles: str, user: discord.Member | None = None) -> None:
        server = await require_server(interaction)
        if server is None: return
        issuer = interaction.user
        assert isinstance(issuer, discord.Member)

        await interaction.response.defer(thinking=True)

        if user is None: user = issuer

        user_roles = self.get_user_roles(user)
        await user.remove_roles(*user_roles, reason=f"/roles set used by {issuer.display_name} ({issuer.id})")

        roles_to_add, could_not_add = self.get_discord_roles(roles, server)

        async with self.bot.database.get_session() as session:
            user_dao = UserDAO(session)
            user_db = await user_dao.get_user_info(user.id)
            user_msg_count = 0 if not user_db else user_db.message_count

        if user_msg_count >= 500:
            regular_role = server.get_role(self.bot.config['rl_id']['regular'])
            if regular_role is not None: roles_to_add.append(regular_role)
        else:
            new_role = server.get_role(self.bot.config['rl_id']['new'])
            if new_role is not None: roles_to_add.append(new_role)

        await user.add_roles(*roles_to_add,
                             reason=f"/roles add_roles used by {issuer.display_name} ({issuer.id})")
        await interaction.followup.send(
            f"Roles added to {user.display_name}.{f" Could not add: {", ".join(could_not_add)}" if len(could_not_add) != 0 else ""}")

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def saved(self, interaction: discord.Interaction[TranspeakBot], user: discord.User | discord.Member | None) -> None:
        server = await require_server(interaction)
        if server is None: return

        issuer = interaction.user
        assert isinstance(issuer, discord.Member)
        if user is None: user = issuer

        async with self.bot.database.get_session() as session:
            role_dao = RoleDAO(session)
            roles = await role_dao.get_saved_roles(user.id, server)

        if len(roles) == 0:
            await interaction.response.send_message(f"Could not find any saved roles for user {user.display_name}")
            return

        await interaction.response.send_message(f"**{user.display_name}'s saved roles:**\n"
                                                f"{", ".join([role.name for role in roles])}")

async def setup(bot: TranspeakBot) -> None:
    bot.tree.add_command(Roles(bot))