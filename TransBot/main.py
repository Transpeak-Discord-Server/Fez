import discord
from discord.ext import commands
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# allows TransBot to access the shared folder (e.g. `from shared import helper_funcs`)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TransBot(commands.Bot):

    cogs = [
        "cogs.ban",
    ]

    async def setup_hook(self):
        for cog in self.cogs:
            await self.load_extension(cog)
            print(f"Loaded cog: {cog}")

    async def on_ready(self):
        print(f'{self.user} has finished booting.')

class Main:

    TBOT_DIR = Path(__file__).resolve().parent

    def run(self):
        load_dotenv(dotenv_path=self.TBOT_DIR / '..' / '.env')
        intents = discord.Intents.default()

        token = os.getenv("TBOT_TOKEN")
        if not token:
            raise ValueError("TransBot token not found in .env file.")

        client = TransBot(intents=intents, command_prefix='!')
        client.run(token)

if __name__ == "__main__":
    Main().run()