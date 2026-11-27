# Fez/TransBot - A Discord.py bot for Transpeak
# Copyright (C) 2026 Fez project contributors
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

import datetime
from pathlib import Path

import discord
from discord import app_commands
from dotenv import load_dotenv

from shared.config import Config
from shared.database import data
from shared.database.BanDAO import BanDAO
from shared.database.UserDAO import UserDAO
from shared.database.__main__ import Database, get_database
from shared.database.data import BanType
from shared.transpeak_bot import TranspeakBot
from shared.utils.misc import require_server, get_member_or_user, send_split_message_embeds
from shared.utils.permissions import Level, permission_check, has_permission

config = Config.json_config

env_path = Path(__file__) / ".." / ".env"
env_file = load_dotenv(env_path)

async def get_ban_embed(server: discord.Guild, bot: TranspeakBot, ban_data: data.Ban) -> discord.Embed:
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

    ban_user = await get_member_or_user(server, bot, ban_data.user_id)
    ban_user_str = "Unknown" if not ban_user else f'{ban_user.display_name} ({ban_user.id})'
    ban_user_icon = None if not ban_user else ban_user.display_avatar.url

    ban_issuer = await get_member_or_user(server, bot, ban_data.issuer_id)
    ban_issuer_str = "Unknown" if not ban_issuer else f'{ban_issuer.display_name} ({ban_issuer.id})'
    ban_issuer_icon = None if not ban_issuer else ban_issuer.display_avatar.url

    ban_embed = discord.Embed(
        title=ban_title,
        colour=colour,
        timestamp=ban_data.timestamp
    )
    ban_embed.add_field(name="Reason", value=ban_data.reason)
    ban_embed.add_field(name="Ban ID", value=ban_data.ban_id)
    ban_embed.set_author(name=ban_issuer_str, icon_url=ban_issuer_icon)
    ban_embed.set_footer(text=ban_user_str, icon_url=ban_user_icon)

    return ban_embed

ban_bot: TranspeakBot
ban_database: Database
ban_msg_channel: discord.TextChannel | None = None
appeal_message: str = config['appeal_message']



async def send_appeal(user: discord.Member) -> bool:
    try:
        await user.send(appeal_message)
        return True
    except Exception as e:
        print(f"Failed to send appeal message to user {user.id}: {e}")
        return False



async def handle_appeal(interaction: discord.Interaction[TranspeakBot], user: discord.User | discord.Member, should_send_appeal: bool | None) -> bool:
    if isinstance(user, discord.User):
        await interaction.followup.send("Appeal message not sent, user is not in the server. User has not been banned.")
        return False

    if should_send_appeal:
        success = await send_appeal(user)
        if not success: await interaction.followup.send("Appeal message failed to send. User has not been banned.")
        return success

    one_day = datetime.timedelta(days=1)
    time_since_join: datetime.timedelta
    join_time = user.joined_at
    time_since_join = datetime.timedelta(0) if join_time is None else datetime.datetime.now(tz=datetime.timezone.utc) - join_time

    async with ban_database.get_session() as session:
        user_dao = UserDAO(session)
        user_db = await user_dao.get_user_info(user.id)
        if not user_db: message_count = 0
        else: message_count = user_db.message_count

    if time_since_join >= one_day and message_count >= 50:
        success = await send_appeal(user)
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

def get_ban_message_channel() -> discord.TextChannel:
    global ban_msg_channel
    if ban_msg_channel is not None: return ban_msg_channel
    ban_msg_channel_id = config['ch_id']['#bans-warnings']
    ban_msg_channel_ = ban_bot.get_channel(ban_msg_channel_id)
    if not isinstance(ban_msg_channel_, discord.TextChannel):
        raise ValueError("Could not find #bans-warnings from config ID")
    ban_msg_channel = ban_msg_channel_
    return ban_msg_channel_


async def send_ban_message(server: discord.Guild, ban_data: data.Ban) -> None:
    ban_embed = await get_ban_embed(server, ban_bot, ban_data)
    channel = get_ban_message_channel()
    await channel.send(embed=ban_embed)


@app_commands.command()
@permission_check(Level.STAFF)
async def ban(interaction: discord.Interaction[TranspeakBot], user: discord.User | discord.Member, reason: str, delete_messages: bool = False, send_ban_appeal: bool | None = None) -> None:

    # This command can take a little while, so we tell Discord we are still doing stuff so it doesn't timeout
    await interaction.response.defer(thinking=True)

    server = await require_server(interaction)
    if server is None: return None

    if isinstance(user, discord.Member) and has_permission(user, Level.STAFF):
        await interaction.followup.send("No.")
        return None

    if send_ban_appeal is None or send_ban_appeal:
        if not await handle_appeal(interaction, user, send_ban_appeal): return None

    async with ban_database.get_session() as session:
        ban_dao = ban_database.ban_dao(session)
        result = await ban_dao.add_ban(user.id, reason, interaction.user.id, BanType.Permanent)

    await send_ban_message(server, result)
    ban_embed = await get_ban_embed(server, ban_bot, result)

    num_messages_delete = 7 if delete_messages else 0
    await server.ban(user, delete_message_days=num_messages_delete, reason=f'Banned by {interaction.user.display_name} ({interaction.user.id}), reason: {reason}')
    await interaction.followup.send(f"Banned {user.display_name} ({user.id})", embed=ban_embed)

    return None

@app_commands.command()
@permission_check(Level.ADMIN)
async def unban(interaction: discord.Interaction[TranspeakBot], user: discord.User | discord.Member, reason: str | None) -> None:
    server = await require_server(interaction)
    if not server: return
    try:
        await server.unban(user, reason=f'Unbanned by {interaction.user.display_name} ({interaction.user.id}), reason: {reason}')
        await interaction.response.send_message(f"Unbanned {user.display_name} ({user.id})")
    except discord.NotFound:
        await interaction.response.send_message("User is not banned.")


class Bans(app_commands.Group):

    bot: TranspeakBot
    database: Database

    def __init__(self, bot: TranspeakBot):
        super().__init__()
        self.bot = bot
        self.database = get_database()

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def get(self, interaction: discord.Interaction[TranspeakBot], user: discord.User | discord.Member) -> None:
        server = await require_server(interaction)
        if server is None: return

        async with self.database.get_session() as session:
            ban_dao = BanDAO(session)
            user_bans = await ban_dao.get_bans(user.id)

        display_name = user.display_name

        if len(user_bans) == 0:
            await interaction.response.send_message("This user has no reported bans")
            return

        embeds: list[discord.Embed] = []
        for ban in user_bans:
            ban_embed = await get_ban_embed(server, self.bot, ban)
            embeds.append(ban_embed)

        channel = interaction.channel
        if not isinstance(channel, discord.abc.Messageable):
            await interaction.response.send_message("Cannot send messages here")
            return

        await interaction.response.send_message("Sending...", ephemeral=True)

        await send_split_message_embeds(channel, f"Bans for user: {display_name}", embeds)

    @app_commands.command()
    @permission_check(Level.STAFF)
    async def edit(self, interaction: discord.Interaction[TranspeakBot], ban_id: int, reason: str) -> None:
        server = await require_server(interaction)
        if not server: return
        try:
            async with self.database.get_session() as session:
                ban_dao = BanDAO(session)
                ban = await ban_dao.edit_ban(ban_id, reason=reason)
            ban_embed = await get_ban_embed(server, self.bot, ban)
            await interaction.response.send_message("Ban updated.", embed=ban_embed)
        except ValueError:
            await interaction.response.send_message("Ban not found.")


async def setup(bot: TranspeakBot) -> None:
    global ban_bot, ban_database
    ban_bot = bot
    ban_database = get_database()
    bot.tree.add_command(ban)
    bot.tree.add_command(unban)
    bot.tree.add_command(Bans(bot))