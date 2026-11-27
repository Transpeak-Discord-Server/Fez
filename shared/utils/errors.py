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


class NotInServerError(AppCommandError):

    def __init__(self, message: str = "This command can only be used within Transpeak."):
        self.message = message


class ConfigError(Exception):

    def __init__(self, message: str = "Invalid bot config"):
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"ConfigError: {self.message}"


class UserPermissionsError(app_commands.CheckFailure):

    def __init__(self, required_perms: "Level"):
        self.required_perms = required_perms
        super().__init__(f"User tried to use a command for {required_perms.name}")


### Error handlers ###

async def tree_error(interaction: discord.Interaction[Any], error: Exception) -> None:
    if isinstance(error, UserPermissionsError):
        await permission_error(interaction, error)
    if isinstance(error, NotInServerError):
        await not_in_server_error(interaction, error)
    print(error)

async def command_error(ctx: commands.Context[Any], error: Exception) -> None:
    if isinstance(error, commands.CommandNotFound):
        return None
    if isinstance(error, UserPermissionsError):
        await permission_error(ctx, error)
    print(error)
    return None

async def permission_error(context: commands.Context[Any] | discord.Interaction[Any], error: UserPermissionsError) -> None:
    from shared.utils.permissions import Level

    if error.required_perms == Level.REGISTERED:
        msg = "You need to be registered to do that! Please ping a staff member for help."
    else:
        msg = f"You need to be a {error.required_perms} to do that!"

    if isinstance(context, discord.Interaction):
        await context.response.send_message(msg)
        return
    await context.reply(msg)

async def not_in_server_error(interaction: discord.Interaction[Any], error: NotInServerError) -> None:
    if interaction.response.is_done():
        await interaction.followup.send(error.message)
        return
    await interaction.response.send_message(error.message)
