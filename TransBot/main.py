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

from typing import List, Any

import discord
from discord.ext import commands
import os
from pathlib import Path
from dotenv import load_dotenv

from shared.utils.misc import shared_error


class TransBot(commands.Bot):

    bot_cogs: List[str] = [
        '.cogs.ban'
    ]

    async def setup_hook(self) -> None:
        for cog in self.bot_cogs:
            await self.load_extension(cog, package=__package__)
            print(f"Loaded cog: {cog}")

    async def on_ready(self) -> None:
        print(f'{self.user} has finished booting.')

    async def on_command_error(self, ctx: commands.Context[Any], error: Exception) -> None:
        await shared_error(ctx, error)

class Main:

    TBOT_DIR = Path(__file__).resolve().parent

    def run(self) -> None:
        load_dotenv(dotenv_path=self.TBOT_DIR / '..' / '.env')
        intents = discord.Intents.all()

        token = os.getenv("TBOT_TOKEN")
        if not token:
            raise ValueError("TransBot token not found in .env file.")

        discord.utils.setup_logging()

        client = TransBot(intents=intents, command_prefix='!')
        client.run(token)

if __name__ == "__main__":
    Main().run()