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
from typing import Any, TYPE_CHECKING

import discord
from discord import app_commands
from discord.app_commands import AppCommandError
from discord.ext import commands

if TYPE_CHECKING:
    from shared.utils.permissions import Level

class CanSendUserError(Exception):
    user_message: str
    async def send(self, interaction: discord.Interaction[Any] | commands.Context[Any]):
        if isinstance(interaction, discord.Interaction):
            if interaction.response.is_done():
                await interaction.followup.send(self.user_message)
                return
            await interaction.response.send_message(self.user_message)
            return
        await interaction.reply(self.user_message)


class NotInServerError(AppCommandError, CanSendUserError):

    def __init__(self, message: str = "This command can only be used within Transpeak."):
        self.user_message = message


class ConfigError(CanSendUserError):

    def __init__(self, message: str = "Invalid bot config"):
        self.user_message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"ConfigError: {self.user_message}"


class UserPermissionsError(app_commands.CheckFailure, CanSendUserError):

    def __init__(self, required_perms: "Level"):
        from shared.utils.permissions import Level

        if required_perms == Level.REGISTERED:
            self.user_message = "You need to be registered to do that! Please ping a staff member for help."
        else:
            self.user_message = f"You need to be a {required_perms} to do that!"
        self.required_perms = required_perms
        super().__init__(f"User tried to use a command for {required_perms.name}")


### Error handlers ###

async def tree_error(interaction: discord.Interaction[Any], error: Exception) -> None:
    if isinstance(error, CanSendUserError):
        await error.send(interaction)
    print(error)

async def command_error(ctx: commands.Context[Any], error: Exception) -> None:
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, CanSendUserError):
        await error.send(ctx)
    print(error)
