import discord
from discord.ext import commands
import os
from pathlib import Path
from dotenv import load_dotenv

class TransBot(commands.Bot):

    cogs = [

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
        intents = discord.Intents.all()

        token = os.getenv("TBOT_TOKEN")
        if not token:
            raise ValueError("TransBot token not found in .env file.")

        client = TransBot(intents=intents, command_prefix='!')
        client.run(token)

if __name__ == "__main__":
    Main().run()