import datetime

import discord
from discord import app_commands, ForumChannel
from discord.ext import commands

from shared.config import Config
from shared.database import data
from shared.database.MessageCountDAO import MessageCountDAO
from shared.database.UserDAO import UserDAO
from shared.database.__main__ import Database, get_database
from shared.utils.misc import require_server, get_member_or_user
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
    @permission_check(Level.REGISTERED)
    async def week(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member | None = None) -> None:
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
            user_info = await user_dao.get_message_count_week(user.id)

        await interaction.response.send_message(f"**{user.display_name}'s message count for this week:** {user_info}")
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

    @app_commands.command()
    @permission_check(Level.REGISTERED)
    async def top_10(self, interaction: discord.Interaction[commands.Bot]) -> None:
        server = await require_server(interaction)
        if not server: return

        await interaction.response.defer(thinking=True)

        async with self.database.get_session() as session:
            msg_count_dao = MessageCountDAO(session)
            top_10_users = await msg_count_dao.get_top_10()

        top_10_msg = f"**Top 10 users by message count:**\n"

        for user_data in top_10_users:
            user = await get_member_or_user(server, self.bot, user_data.id)
            if not user: user_name = "Unknown"
            else: user_name = user.display_name
            if user == interaction.user:
                its_you = " **<--- You**"
            else:
                its_you = ""
            top_10_msg += f"{user_name}: {user_data.message_count}{its_you}\n"

        await interaction.followup.send(top_10_msg)

    @app_commands.command()
    @permission_check(Level.REGISTERED)
    async def top_10_week(self, interaction: discord.Interaction[commands.Bot]) -> None:
        server = await require_server(interaction)
        if not server: return

        await interaction.response.defer(thinking=True)

        async with self.database.get_session() as session:
            msg_count_dao = MessageCountDAO(session)
            top_10_users = await msg_count_dao.get_top_10_week()

        top_10_msg = f"**Top 10 users by message count this week:**\n"

        for user_data in top_10_users:
            user = await get_member_or_user(server, self.bot, user_data.user_id)
            if not user:
                user_name = "Unknown"
            else:
                user_name = user.display_name
            if user == interaction.user: its_you = " **<--- You**"
            else: its_you = ""
            top_10_msg += f"{user_name}: {user_data.count}{its_you}\n"

        await interaction.followup.send(top_10_msg)


    @staticmethod
    async def check_verified(server: discord.Guild, message: discord.Message, user_info: data.User) -> None:
        new_role = server.get_role(config['rl_id']['new'])
        regular_role = server.get_role(config['rl_id']['regular'])

        if new_role is None or regular_role is None: return

        author = message.author
        if isinstance(author, discord.Member) and author.joined_at is not None and new_role in author.roles:
            time_since_join = datetime.datetime.now() - author.joined_at
            if user_info.message_count >= 500 and time_since_join > datetime.timedelta(days=1):
                await author.remove_roles(new_role)
                await author.add_roles(regular_role)
                await message.reply("You are now verified and can opt in to regular-only channels.")

    async def update_message_count(self, channel: discord.TextChannel | discord.VoiceChannel | discord.StageChannel | discord.Thread, server: discord.Guild, author: discord.User | discord.Member) -> None:
        for ignored_channel in config['ignored_channels']:
            if config['ch_id'][ignored_channel] == channel.id:
                return

        permission_channel: discord.TextChannel | discord.VoiceChannel | discord.StageChannel | ForumChannel
        if isinstance(channel, discord.Thread):
            permission_channel_ = channel.parent
            if permission_channel_ is None: return
            permission_channel = permission_channel_
        else:
            permission_channel = channel

        ignore_messages_role = self.get_ignore_messages_role(server)
        ignore_overwrites = permission_channel.overwrites_for(ignore_messages_role)
        if not ignore_overwrites.is_empty(): return

        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            await user_dao.increment_message_count(author.id)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        server = message.guild
        if server is None: return

        channel = message.channel
        if isinstance(channel, discord.DMChannel | discord.GroupChannel | discord.PartialMessageable): return

        if message.author.bot:
            return

        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            user_info = await user_dao.set_last_message(message.author.id, message.content)

        await self.update_message_count(channel, server, message.author)

        await self.check_verified(server, message, user_info)

        if user_info.message_count % 1000 == 0 and isinstance(channel, discord.TextChannel | discord.VoiceChannel):
            await channel.send(f"**:trophy: {message.author.display_name} has reached {user_info.message_count} messages!**")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MessageCount(bot))