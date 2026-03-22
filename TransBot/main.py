import discord
from discord.ext import commands
import os
from pathlib import Path
from dotenv import load_dotenv
from shared.utils.permissions import UserPermissionsError

class TransBot(commands.Bot):

    cogs = [
        # '.cogs.ban',
        # '.cogs.
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

    TBOT_DIR = Path(__file__).resolve().parent

    def run(self):
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