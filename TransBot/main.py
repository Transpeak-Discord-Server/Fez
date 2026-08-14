from typing import List, Any

import discord
from discord.ext import commands
import os
from pathlib import Path
from dotenv import load_dotenv

from shared.utils.misc import shared_error


class TransBot(commands.Bot):

    # Cogs to be added when db support is ready:
    # '.cogs.ban'

    bot_cogs: List[str] = [

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