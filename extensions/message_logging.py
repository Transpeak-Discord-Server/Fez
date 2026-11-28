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

import discord
from dataclasses import dataclass
from discord import TextChannel, DMChannel, GroupChannel
from discord.abc import GuildChannel
from discord.ext import commands

from shared.transpeak_bot import TranspeakBot
from shared.utils.errors import ConfigError
from shared.utils.user_info import is_on_wl
import os

CURRENT_PATH = os.path.dirname(__file__)

@dataclass
class LoggingDetails:
    title: str
    colour: discord.Colour

class MessageLogging(commands.Cog):

    ON_MESSAGE_DETAILS = LoggingDetails(
        title='Message sent 💬',
        colour=discord.Colour.blue()
    )

    ON_EDIT_DETAILS = LoggingDetails(
        title='Message edited 📝',
        colour=discord.Colour.orange()
    )

    ON_DELETE_DETAILS = LoggingDetails(
        title='Message deleted ❌',
        colour=discord.Colour.red()
    )

    def __init__(self, bot: TranspeakBot) -> None:
        self.bot_dms: TextChannel | None = None
        self.unified_nsfw: TextChannel | None = None
        self.unified_sfw: TextChannel | None = None
        self.staff_unified: TextChannel | None = None
        self.bot = bot

        self.UNIFIED_SFW_ID = self.bot.config['ch_id']['#unified-chat-sfw']
        self.UNIFIED_NSFW_ID = self.bot.config['ch_id']['#unified-chat-nsfw']
        self.STAFF_UNIFIED_ID = self.bot.config['ch_id']['#unified-chat-staff']
        self.BOT_DMS_ID = self.bot.config['ch_id']['#bot-dms']

        self.STAFF_CHANNELS = [self.bot.config['ch_id'][x] for x in self.bot.config['staff_channels']]
        self.NSFW_CHANNELS = [self.bot.config['ch_id'][x] for x in self.bot.config['nsfw_channels']]
        self.IGNORED_CHANNELS = [self.bot.config['ch_id'][x] for x in self.bot.config['logging_ignored_channels']]

    async def cog_load(self) -> None:
        unified_sfw = await self.bot.fetch_channel(self.UNIFIED_SFW_ID)
        if not isinstance(unified_sfw, TextChannel):
            raise ConfigError("Unified SFW channel not found")
        self.unified_sfw = unified_sfw

        unified_nsfw = await self.bot.fetch_channel(self.UNIFIED_NSFW_ID)
        if not isinstance(unified_nsfw, TextChannel):
            raise ConfigError("Unified NSFW channel not found")
        self.unified_nsfw = unified_nsfw

        bot_dms = await self.bot.fetch_channel(self.BOT_DMS_ID)
        if not isinstance(bot_dms, TextChannel):
            raise ConfigError("#bot-dms channel not found")
        self.bot_dms = bot_dms

        staff_unified = await self.bot.fetch_channel(self.STAFF_UNIFIED_ID)
        if not isinstance(staff_unified, TextChannel):
            raise ConfigError("Staff Unified not found")
        self.staff_unified = staff_unified

    def log_message_in(self, channel: discord.abc.Messageable) -> discord.TextChannel | None:
        if isinstance(channel, DMChannel | GroupChannel):
            return self.bot_dms
        if not isinstance(channel, GuildChannel):
            return None
        if channel.id in self.STAFF_CHANNELS:
            return self.staff_unified
        if isinstance(channel, TextChannel) and (channel.id in self.NSFW_CHANNELS or channel.is_nsfw()):
            return self.unified_nsfw
        if channel.id in self.IGNORED_CHANNELS:
            return None
        return self.unified_sfw

    @staticmethod
    async def log_embed(message: discord.Message, description: str, title: str, colour: discord.Colour) -> discord.Embed:
        is_on_watchlist = ':children_crossing:' if is_on_wl(message.author) else ''
        embed = discord.Embed(
            title=title,
            description=description,
            colour=colour
        )

        embed.set_author(name=f'{is_on_watchlist} {message.author.display_name} ({message.author.id})',
                         icon_url=message.author.display_avatar.url)

        if message.guild and not isinstance(message.channel, DMChannel | GroupChannel):
            channel = message.channel.mention
        else:
            channel = "DMs"
        embed.add_field(name="Channel", value=channel)

        if message.attachments:
            links = "\n".join(attachment.url for attachment in message.attachments)
            embed.add_field(name="Attachments", value=links, inline=False)

        return embed

    async def log(self, message:discord.Message, title: str, colour: discord.Colour, description: str | None) -> None:
        if message.author.bot: return None
        if description is None: return None

        send_in = self.log_message_in(message.channel)
        if not send_in: return None

        embed = await self.log_embed(message, description, title, colour)

        await send_in.send(embed=embed)
        return None

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:

        if before.pinned != after.pinned:
            description = f"Message was pinned"
        elif before.content != after.content:
            description = f"**Before**\n{before.content}\n**After**\n{after.content}"
        else:
            description = None

        await self.log(after, self.ON_EDIT_DETAILS.title, self.ON_EDIT_DETAILS.colour, description)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        await self.log(message, self.ON_DELETE_DETAILS.title, self.ON_DELETE_DETAILS.colour, message.content)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if not isinstance(message.channel, DMChannel | GroupChannel): return
        await self.log(message, self.ON_MESSAGE_DETAILS.title, self.ON_MESSAGE_DETAILS.colour, message.content)

async def setup(bot: TranspeakBot) -> None:
    await bot.add_cog(MessageLogging(bot))