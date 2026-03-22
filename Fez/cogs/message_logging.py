import discord
from discord.ext import commands
from shared.utils.user_info import is_on_wl
import os
import json
CURRENT_PATH = os.path.dirname(__file__)
with open(os.path.join(CURRENT_PATH,"../../shared/bot_config.json"), "r") as f:
    config = json.load(f)

class MessageLogging(commands.Cog):

    UNIFIED_SFW_ID = config['ch_id']['#unified-chat-sfw']
    UNIFIED_NSFW_ID = config['ch_id']['#unified-chat-nsfw']
    STAFF_UNIFIED_ID = config['ch_id']['#unified-chat-staff']
    BOT_DMS_ID = config['ch_id']['#bot-dms']
    STAFF_CHANNELS = config["staff_channels"]
    NSFW_CHANNELS = config["nsfw_channels"]
    IGNORED_CHANNELS = config["ignored_channels"]

    def __init__(self, bot):
        self.bot_dms = None
        self.unified_nsfw = None
        self.unified_sfw = None
        self.staff_unified = None
        self.bot = bot

    async def cog_load(self):
        self.unified_sfw = await self.bot.fetch_channel(self.UNIFIED_SFW_ID)
        if not self.unified_sfw:
            print("Unified SFW channel not found")
        self.unified_nsfw = await self.bot.fetch_channel(self.UNIFIED_NSFW_ID)
        if not self.unified_nsfw:
            print("Unified NSFW channel not found")
        self.bot_dms = await self.bot.fetch_channel(self.BOT_DMS_ID)
        if not self.bot_dms:
            print("Bot DMs channel not found")
        self.staff_unified = await self.bot.fetch_channel(self.STAFF_UNIFIED_ID)
        if not self.staff_unified:
            print("Staff United channel not found")

    def log_message_in(self, channel: discord.TextChannel) -> discord.TextChannel | None:
        if not channel.guild:
            return self.bot_dms
        if channel.id in self.STAFF_CHANNELS:
            return self.staff_unified
        if channel.id in self.NSFW_CHANNELS or channel.is_nsfw():
            return self.unified_nsfw
        if channel.id in self.IGNORED_CHANNELS:
            return None
        return self.unified_sfw

    @staticmethod
    async def send_log(message: discord.Message, send_in: discord.TextChannel | None):
        if not send_in:
            return None
        _is_wl = ':children_crossing:' if is_on_wl(message.author) else ''
        embed = discord.Embed(
            description = message.content,
            color = discord.Color.blurple()
        )
        embed.set_author(name=f'{_is_wl} {message.author.display_name} ({message.author.id})', icon_url=message.author.display_avatar.url)
        embed.add_field(name="Channel", value=message.channel.mention if message.guild else "DMs")

        if message.attachments:
            links = "\n".join(attachment.url for attachment in message.attachments)
            embed.add_field(name="Attachments", value=links, inline=False)

        return await send_in.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return None
        return await self.send_log(message, self.log_message_in(message.channel))

async def setup(bot):
    await bot.add_cog(MessageLogging(bot))