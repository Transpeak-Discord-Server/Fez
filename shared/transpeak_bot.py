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

from typing import Any

import discord
from discord import app_commands, Interaction
from discord.app_commands import AppCommandError
from discord.ext import commands

from shared.config import Config
from shared.database.__main__ import get_database
from shared.utils.misc import tree_error, shared_error


class TranspeakBotTree(app_commands.CommandTree):
    async def on_error(self, interaction: Interaction[Any], error: AppCommandError, /) -> None:
        await tree_error(interaction, error)

class TranspeakBot(commands.Bot):
    """Only includes things common to any bot on Transpeak.
    The bot in extensions can be typed as TranspeakBot (instead of commands.Bot) for easy access to the database."""

    database = get_database()
    config = Config.json_config

    def __init__(self, bot_extensions: list[str], intents: discord.Intents, **kwargs: Any):
        # noinspection PyTypeChecker
        super().__init__(command_prefix="!", tree_cls=TranspeakBotTree, intents=intents, **kwargs)
        self.bot_extensions = bot_extensions

    async def setup_hook(self) -> None:

        for extension in self.bot_extensions:
            try:
                await self.load_extension(extension, package=__package__)
                print(f"Loaded extension: {extension}")
            except commands.ExtensionError as e:
                print(f"Failed to load extension {extension}: {e}")
        print("Syncing...")
        await self.tree.sync()
        print("Successfully synced!")

    async def on_ready(self) -> None:
        print(f'{self.user} has finished booting.')

    async def on_command_error(self, ctx: commands.Context[Any], error: Exception) -> None:
        await shared_error(ctx, error)