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
import os
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv

from shared.utils.misc import shared_error




class Fez(commands.Bot):

    bot_cogs = [
        '.cogs.staff_commands',
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
    FEZ_DIR = Path(__file__).resolve().parent

    def run(self) -> None:
        load_dotenv(dotenv_path=self.FEZ_DIR / '..' / '.env')

        intents = discord.Intents.all()

        token = os.getenv("FEZ_TOKEN")
        if not token:
            raise ValueError("Fez token not found in .env file.")

        discord.utils.setup_logging()

        client = Fez(intents=intents, command_prefix='!')
        client.run(token)

if __name__ == "__main__":
    Main().run()