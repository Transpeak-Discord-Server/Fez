import discord
from discord import app_commands
from discord.ext import commands

from shared.config import Config
from shared.database.UserDAO import UserDAO
from shared.database.__main__ import Database, get_database
from shared.utils.misc import require_server
from shared.utils.permissions import permission_check, Level, has_permission

config = Config.json_config

class MessageCount(commands.GroupCog):

    bot: commands.Bot
    database: Database
    ignore_messages_role: discord.Role | None = None

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = get_database()

    @app_commands.command()
    @permission_check(Level.REGISTERED)
    async def get(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member | None = None) -> None:
        server = await require_server(interaction)
        if server is None: return None

        interaction_user = interaction.user
        if isinstance(interaction_user, discord.User):
            await interaction.response.send_message("Something went wrong. Please try again.")
            return None

        if user is not None and not has_permission(interaction_user, Level.STAFF):
            await interaction.response.send_message("You do not have permission to get the message counts of other users.")
            return None

        if user is None: user = interaction_user

        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            user_info = await user_dao.get_user_info(user.id)

        if user_info is None:
            await interaction.response.send_message("User has no message count.")
            return None

        await interaction.response.send_message(f"**{user.display_name}'s message count:** {user_info.message_count}")
        return None

    @app_commands.command()
    @permission_check(Level.LEAD)
    async def set(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member, count: int) -> None:
        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            await user_dao.set_message_count(user.id, count)
        await interaction.response.send_message(f"{user.display_name}'s message count set to {count}")

    def get_ignore_messages_role(self, server: discord.Guild) -> discord.Role:
        if self.ignore_messages_role is not None:
            return self.ignore_messages_role
        ignore_messages_role = server.get_role(config['rl_id']['ignore-messages'])
        if ignore_messages_role is None:
            raise ValueError("Could not find ignore-messages role")
        self.ignore_messages_role = ignore_messages_role
        return ignore_messages_role

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        server = message.guild
        if server is None: return

        channel = message.channel
        if isinstance(channel, discord.DMChannel | discord.GroupChannel): return

        if message.author.bot:
            return

        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            await user_dao.set_last_message(message.author.id, message.content)

        for ignored_channel in config['ignored_channels']:
            if config['ch_id'][ignored_channel] == channel.id:
                return

        if isinstance(channel, discord.Thread):
            parent_channel = channel.parent
            if parent_channel is None: return
            channel = parent_channel

        ignore_messages_role = self.get_ignore_messages_role(server)
        ignore_overwrites = channel.overwrites_for(ignore_messages_role)
        if not ignore_overwrites.is_empty(): return

        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            await user_dao.increment_message_count(message.author.id)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MessageCount(bot))