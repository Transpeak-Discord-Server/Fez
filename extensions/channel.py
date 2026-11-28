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

import dataclasses

import discord
from discord import app_commands

from shared.transpeak_bot import TranspeakBot
from shared.utils.misc import require_server
from shared.utils.permissions import permission_check, Level, has_permission

@dataclasses.dataclass
class RoleLevelPair:
    role: discord.Role
    level: Level

class Channel(app_commands.Group):

    bot: TranspeakBot

    def __init__(self, bot: TranspeakBot):
        super().__init__()
        self.bot = bot

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def slow_mode(self, interaction: discord.Interaction[TranspeakBot], delay: int | None = None) -> None:
        channel = interaction.channel
        if not isinstance(channel, discord.TextChannel | discord.Thread | discord.VoiceChannel):
            await interaction.response.send_message("Cannot set slow mode in this channel!")
            return

        if delay is None:
            await channel.edit(slowmode_delay=0)
            await interaction.response.send_message("Slow mode disabled for this channel")
            return

        if delay < 0 or delay > 21600:
            await interaction.response.send_message("Delay must be between 0 and 21600 seconds (inclusive)")
            return

        await channel.edit(slowmode_delay=delay)

        await interaction.response.send_message(f"Slow mode set to {delay} seconds.")

    async def disable_staff_only(self, interaction: discord.Interaction[TranspeakBot], server: discord.Guild, channel: discord.TextChannel | discord.VoiceChannel, role_level: RoleLevelPair | None = None) -> None:
        overwrites = dict(channel.overwrites)

        staff_role = server.get_role(self.bot.config['rl_id']['staff'])
        if not staff_role:
            await interaction.response.send_message("Could not find staff role from bot config")
            return

        if role_level is None:
            role_level = RoleLevelPair(staff_role, Level.STAFF)

        for role, perm in overwrites.items():
            if isinstance(role, discord.Member) and not has_permission(role, role_level.level) and perm.view_channel is True:
                overwrites[role].update(send_messages=True)

            if isinstance(role, discord.Role) and role < role_level.role and perm.view_channel is True:

                # New members can view trans-resources, but can't send anything. TODO: Make this not hardcoded.
                if channel.id == self.bot.config['ch_id']['#trans-resources'] and role.id == self.bot.config['rl_id']['new']:
                    continue

                overwrites[role].update(send_messages=True)

        await channel.edit(overwrites=overwrites)

        await interaction.response.send_message("Staff only mode has been disabled for this channel.")

    async def enable_staff_only(self, interaction: discord.Interaction[TranspeakBot], server: discord.Guild, channel: discord.TextChannel | discord.VoiceChannel, role_level: RoleLevelPair | None = None) -> None:
        overwrites = dict(channel.overwrites)

        staff_role = server.get_role(self.bot.config['rl_id']['staff'])
        if not staff_role:
            await interaction.response.send_message("Could not find staff role from bot config")
            return

        if not role_level:
            role_level = RoleLevelPair(staff_role, Level.STAFF)

        for role, perm in overwrites.items():
            if isinstance(role, discord.Member) and not has_permission(role, role_level.level) and perm.view_channel == True:
                overwrites[role].update(send_messages=False)

            if isinstance(role, discord.Role) and role < role_level.role and perm.view_channel == True:
                overwrites[role].update(send_messages=False)

        await channel.edit(overwrites=overwrites)

        await interaction.response.send_message("Staff only mode has been enabled for this channel.")

    async def get_is_staff_only(self, interaction: discord.Interaction[TranspeakBot], server: discord.Guild, channel: discord.TextChannel | discord.VoiceChannel, role_level: RoleLevelPair | None = None) -> bool | None:
        staff_role = server.get_role(self.bot.config['rl_id']['staff'])
        if not staff_role:
            await interaction.response.send_message("Could not find staff role from bot config")
            return None

        if role_level is None:
            role_level = RoleLevelPair(staff_role, Level.STAFF)

        is_staff_only = True
        for role, perm in channel.overwrites.items():
            if isinstance(role, discord.Member) and not has_permission(role, role_level.level) and perm.send_messages == True:
                is_staff_only = False
                break

            if isinstance(role, discord.Role) and role < role_level.role and perm.send_messages == True:
                is_staff_only = False
                break

        return is_staff_only

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def staff_only(self, interaction: discord.Interaction[TranspeakBot], channel: discord.TextChannel | discord.VoiceChannel | None = None) -> None:
        server = await require_server(interaction)

        if channel is None:
            interaction_channel = interaction.channel
            if not isinstance(interaction_channel, discord.TextChannel | discord.VoiceChannel):
                await interaction.response.send_message("Cannot set staff only in this channel!")
                return
            channel = interaction_channel

        staff_role = server.get_role(self.bot.config['rl_id']['staff'])
        if not staff_role:
            await interaction.response.send_message("Could not find staff role from bot config")
            return

        is_staff_only = await self.get_is_staff_only(interaction, server, channel)
        if is_staff_only is None: return

        # Disable staff only
        if is_staff_only:
            await self.disable_staff_only(interaction, server, channel)
            return

        await self.enable_staff_only(interaction, server, channel)

async def setup(bot: TranspeakBot) -> None:
    bot.tree.add_command(Channel(bot))