import datetime
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from shared.config import Config
from shared.database import data
from shared.database.UserDAO import UserDAO
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
    ban_msg_channel: discord.TextChannel | None
    appeal_message: str = 'You have been removed from Transpeak. Should you wish to appeal this ban, please read the information below and follow the guidelines.\n' \
                          'An appeal can be granted for two reasons: (1) You feel your ban was unjustified; (2) You feel you have reformed and are able to take place on the server once again.\n' \
                          'If you are requesting an appeal because you feel your ban was unjustified, you may make your request immediately. However, if you are requesting an appeal due to reformation you will be required to wait at least six months before the appeal will be looked at.\n' \
                          'You may only send in one reform appeal, and one unjust appeal. If both of these get denied, you are not eligible for any future appeals.' \
                          'Please note that if you have previously been unbanned due to a reformation appeal and now have been banned again, ***you may not appeal your ban again.***\n' \
                          'To request an appeal join the following server and follow the instructions found in #welcome: https://discord.gg/SWFufu7cp2\n\n'

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = get_database()

    async def send_appeal(self, user: discord.Member) -> bool:
        try:
            await user.send(self.appeal_message)
            return True
        except Exception as e:
            print(f"Failed to send appeal message to user {user.id}: {e}")
            return False



    async def handle_appeal(self, interaction: discord.Interaction[commands.Bot], user: discord.User | discord.Member, send_appeal: bool | None) -> bool:
        if isinstance(user, discord.User):
            return True if not send_appeal else False

        if send_appeal:
            success = await self.send_appeal(user)
            if not success: await interaction.followup.send("Appeal message failed to send. User has not been banned.")
            return success

        one_day = datetime.timedelta(days=1)
        time_since_join: datetime.timedelta
        join_time = user.joined_at
        time_since_join = datetime.timedelta(0) if join_time is None else datetime.datetime.now(tz=datetime.timezone.utc) - join_time

        async with self.database.get_session() as session:
            user_dao = UserDAO(session)
            user_db = await user_dao.get_user_info(user.id)
            if not user_db: message_count = 0
            else: message_count = user_db.message_count

        if time_since_join >= one_day and message_count >= 50:
            success = await self.send_appeal(user)
            if success:
                await interaction.followup.send("Appeal message sent")
            else:
                await interaction.followup.send("Appeal message failed to send. User has not been banned.")
            return success

        if time_since_join < one_day and message_count < 50:
            await interaction.followup.send("Appeal message not sent. User has been in the server for less than a day and has less than 50 messages.")
        elif time_since_join < one_day:
            await interaction.followup.send("Appeal message not sent. User has sent 50 messages, but has not been in the server for more than a day.")
        else:
            await interaction.followup.send("Appeal message not sent. User has been in the server for over a day, but has not sent 50 messages.")

        return True

    def get_ban_message_channel(self) -> discord.TextChannel:
        if self.ban_msg_channel is not None: return self.ban_msg_channel
        ban_msg_channel_id = config['ch_id']['#bans-warnings']
        ban_msg_channel = self.bot.get_channel(ban_msg_channel_id)
        if not isinstance(ban_msg_channel, discord.TextChannel):
            raise ValueError("Could not find #bans-warnings from config ID")
        self.ban_msg_channel = ban_msg_channel
        return ban_msg_channel


    async def send_ban_message(self, ban_data: data.Ban) -> None:
        ban_title: str
        colour: discord.Colour
        if ban_data.ban_type == BanType.Permanent:
            ban_title = ":b: Permanent Ban issued"
            colour = discord.Colour.red()
        elif ban_data.ban_type == BanType.Temporary:
            ban_title = ":regional_indicator_b: Temporary Ban issued"
            colour = discord.Colour.orange()
        elif ban_data.ban_type == BanType.VC:
            ban_title = ":mute: VC Ban issued"
            colour = discord.Colour.blurple()
        else:
            ban_title = ":mute: :bear: VC Soft Ban issued"
            colour = discord.Colour.blurple()

        transpeak = self.bot.get_guild(config['server_id'])
        if transpeak is None:
            raise RuntimeError("Could not find Transpeak")

        ban_user = await get_member_or_user(transpeak, self.bot, ban_data.user_id)
        ban_user_str = "Unknown" if not ban_user else f'{ban_user.display_name} ({ban_user.id}'
        ban_user_icon = None if not ban_user else ban_user.display_avatar.url

        ban_issuer = await get_member_or_user(transpeak, self.bot, ban_data.issuer_id)
        ban_issuer_str = "Unknown" if not ban_issuer else f'{ban_issuer.display_name} ({ban_issuer.id})'
        ban_issuer_icon = None if not ban_issuer else ban_issuer.display_avatar.url

        ban_embed = discord.Embed(
            title=ban_title,
            colour=colour,
            timestamp=ban_data.timestamp
        )
        ban_embed.add_field(name="Reason", value=ban_data.reason)
        ban_embed.set_author(name=ban_issuer_str, icon_url=ban_issuer_icon)
        ban_embed.set_footer(text=ban_user_str, icon_url=ban_user_icon)

        ban_msg_channel = self.get_ban_message_channel()
        await ban_msg_channel.send(embed=ban_embed)


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
            if not await self.handle_appeal(interaction, user, send_appeal): return None

        async with self.database.get_session() as session:
            ban_dao = self.database.ban_dao(session)
            result = await ban_dao.add_ban(user_id, reason, interaction.user.id, BanType.Permanent)

        await self.send_ban_message(result)

        num_messages_delete = 7 if delete_messages else 0
        await server.ban(user, delete_message_days=num_messages_delete)

        return None






async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))