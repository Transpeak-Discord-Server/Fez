import discord

import os
from pathlib import Path

transbot_dir = Path(__file__).resolve().parent

# Environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path=transbot_dir / '..' / '.env')

class Client(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has finished booting.')

intents = discord.Intents.default()

client = Client(intents=intents)
client.run(os.getenv("TBOT_TOKEN"))

