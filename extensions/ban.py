import os
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy import URL

from shared.config import Config
from shared.database import data
from shared.database.__main__ import Database, get_database
from shared.database.data import BanType
from shared.utils.misc import require_server, get_member_or_user
from shared.utils.permissions import Level, permission_check, has_permission

config = Config.json_config

env_path = Path(__file__) / ".." / ".env"
env_file = load_dotenv(env_path)

class Ban(commands.GroupCog):

    bot: commands.Bot
    database: Database

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = get_database()

    async def handle_appeal(self, user: discord.User | discord.Member) -> bool:
        raise NotImplementedError # just in case i accidentally forget to add this or something lol

    async def send_ban_message(self, ban_data: data.Ban) -> bool:
        raise NotImplementedError

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def ban(self, interaction: discord.Interaction[commands.Bot], user_id: int, reason: str, delete_messages: bool = False, send_appeal: bool | None = None) -> None:

        server = await require_server(interaction)
        if server is None: return None

        user = await get_member_or_user(server, self.bot, user_id)

        if user is None:
            await interaction.response.send_message("Could not find user.")
            return None

        if isinstance(user, discord.Member) and has_permission(user, Level.STAFF):
            await interaction.response.send_message("No.")
            return None

        if not isinstance(user, discord.Member) and send_appeal:
            await interaction.response.send_message("Cannot send appeal, user is not in the server. The user has not been banned.")
            return None

        if send_appeal is None or send_appeal:
            if not await self.handle_appeal(user): return None

        async with self.database.get_session() as session:
            ban_dao = self.database.ban_dao(session)
            result = await ban_dao.add_ban(user_id, reason, interaction.user.id, BanType.Permanent)

        await self.send_ban_message(result)

        num_messages_delete = 7 if delete_messages else 0
        await server.ban(user, delete_message_days=num_messages_delete)

        return None






async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))