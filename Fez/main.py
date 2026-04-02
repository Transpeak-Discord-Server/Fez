# Fez/TransBot - A Discord.py bot for Transpeak
# Copyright (C) 2026 Aven F
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

import discord
import os
from pathlib import Path
from discord.ext import commands
from dotenv import load_dotenv
from shared.utils.permissions import UserPermissionsError

class Fez(commands.Bot):

    cogs = [
        '.cogs.staff_commands',
    ]

    async def setup_hook(self):
        for cog in self.cogs:
            await self.load_extension(cog, package=__package__)
            print(f"Loaded cog: {cog}")

    async def on_ready(self):
        print(f'{self.user} has finished booting.')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return None
        if isinstance(error, UserPermissionsError):
            if error.required_perms == "new":
                return ctx.reply("You need to be registered to do that! Please ping a staff member for help.")
            return ctx.reply(f"You need to be a {error.required_perms} to do that!")
        return print(error)



class Main:
    FEZ_DIR = Path(__file__).resolve().parent

    def run(self):
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