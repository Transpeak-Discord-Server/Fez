import discord
from discord import TextChannel, DMChannel, GroupChannel
from discord.abc import GuildChannel
from discord.ext import commands

from shared.config import Config
from shared.utils.errors import ConfigError
from shared.utils.user_info import is_on_wl
import os

CURRENT_PATH = os.path.dirname(__file__)
config = Config.json_config

class MessageLogging(commands.Cog):

    UNIFIED_SFW_ID = config['ch_id']['#unified-chat-sfw']
    UNIFIED_NSFW_ID = config['ch_id']['#unified-chat-nsfw']
    STAFF_UNIFIED_ID = config['ch_id']['#unified-chat-staff']
    BOT_DMS_ID = config['ch_id']['#bot-dms']
    STAFF_CHANNELS = config["staff_channels"]
    NSFW_CHANNELS = config["nsfw_channels"]
    IGNORED_CHANNELS = config["ignored_channels"]

    def __init__(self, bot: commands.Bot) -> None:
        self.bot_dms: TextChannel | None = None
        self.unified_nsfw: TextChannel | None = None
        self.unified_sfw: TextChannel | None = None
        self.staff_unified: TextChannel | None = None
        self.bot = bot

    async def cog_load(self) -> None:
        united_sfw = await self.bot.fetch_channel(self.UNIFIED_SFW_ID)
        if not isinstance(united_sfw, TextChannel):
            raise ConfigError("United SFW channel not found")
        self.unified_sfw = united_sfw

        united_nsfw = await self.bot.fetch_channel(self.UNIFIED_NSFW_ID)
        if not isinstance(united_nsfw, TextChannel):
            raise ConfigError("United NSFW channel not found")
        self.unified_nsfw = united_nsfw

        bot_dms = await self.bot.fetch_channel(self.BOT_DMS_ID)
        if not isinstance(bot_dms, TextChannel):
            raise ConfigError("#bot-dms channel not found")
        self.bot_dms = bot_dms

        staff_united = await self.bot.fetch_channel(self.STAFF_UNIFIED_ID)
        if not isinstance(staff_united, TextChannel):
            raise ConfigError("Staff United not found")
        self.staff_unified = staff_united

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
    async def log_embed(message: discord.Message, description: str, title: str) -> discord.Embed:
        _is_wl = ':children_crossing:' if is_on_wl(message.author) else ''
        embed = discord.Embed(
            description=description,
            color=discord.Color.blurple()
        )

        embed.set_author(name=f'{_is_wl} {message.author.display_name} ({message.author.id})',
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

    async def log_edit(self, before: discord.Message, after: discord.Message, send_in: discord.TextChannel | None) -> None:
        if not send_in:
            return None

        if before.pinned != after.pinned:
            description = f"Message was pinned"
        elif before.content != after.content:
            description = f"**Before**\n{before.content}\n**After**\n{after.content}"
        else:
            return None

        embed = await self.log_embed(after, description, "Message edited 📝")

        await send_in.send(embed=embed)
        return None

    async def log_send(self, message: discord.Message, send_in: discord.TextChannel | None) -> None:
        if not send_in:
            return None

        embed = await self.log_embed(message, message.content, "Message sent 💬")

        await send_in.send(embed=embed)
        return None

    async def log_delete(self, message: discord.Message, send_in: discord.TextChannel | None) -> None:
        if not send_in:
            return None

        embed = await self.log_embed(message, message.content, "Message deleted ❌")

        await send_in.send(embed=embed)
        return None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:

        if message.author.bot:
            return None
        await self.log_send(message, self.log_message_in(message.channel))
        return None

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        if after.author.bot: return None

        await self.log_edit(before, after, self.log_message_in(after.channel))
        return None

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:

        if message.author.bot:
            return None
        await self.log_delete(message, self.log_message_in(message.channel))
        return None

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MessageLogging(bot))