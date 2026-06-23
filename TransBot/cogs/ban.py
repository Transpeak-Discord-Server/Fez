from datetime import datetime
from time import time
from typing import Any

import discord
from discord import TextChannel
from discord.ext import commands
from discord.ext.commands import Context, CommandError

from shared.config import Config
from shared.database.data import BanData
from shared.database.old_db.database import OldDatabase
from shared.utils.errors import ConfigError
from shared.utils.misc import get_member_or_user
from shared.utils.permissions import permission_check, Level, has_permission


class Ban(commands.Cog):

    flags = ["-nd", "-d"]
    config = Config.json_config

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = OldDatabase()

    @staticmethod
    async def require_server(ctx: Context[Any]) -> discord.Guild | None:
        if ctx.guild is None:
            await ctx.reply("This command can only be used within Transpeak.")
            return None
        return ctx.guild

    async def user_from_arg(self, ctx: Context[Any], server: discord.Guild, arg: str) -> discord.Member | discord.User | None:
        if not arg.isdigit():
            await ctx.reply("Please provide a valid user ID.")
            return None
        user = await get_member_or_user(server, self.bot, int(arg))
        if user is None:
            await ctx.reply("User not found.")
            return None
        return user

    async def ban_embed(self, server: discord.Guild, ban: BanData) -> discord.Embed:

        user = await get_member_or_user(server, self.bot, ban.user)
        banner = await get_member_or_user(server, self.bot, ban.banner)
        if user is None or banner is None: raise CommandError("ban_embed run without valid user and/or banner")

        embed = discord.Embed(
            title=f"{user.display_name} banned",
            description=ban.reason,
            timestamp=datetime.fromtimestamp(ban.timestamp/1000),
            colour=discord.Colour.red()
        )
        embed.set_author(name=user.id, icon_url=user.display_avatar.url)
        embed.add_field(name="Links", value="\n".join(ban.links))
        embed.set_footer(text=banner.display_name, icon_url=banner.display_avatar.url)

        return embed

    async def bans_embeds(self, server: discord.Guild, bans: list[BanData]) -> list[discord.Embed]:

        embeds: list[discord.Embed] = []

        for ban in bans:
            embeds.append(await self.ban_embed(server, ban))

        return embeds

    @classmethod
    async def send_appeal_message(cls, member: discord.Member) -> None | str:
        try:
            await member.send(cls.config["APPEAL_MESSAGE"])
            return None
        except discord.Forbidden as e:
            return "Could not send appeal message. Reason: " + str(e)
        except discord.HTTPException as e:
            return "Could not send appeal message. Reason: " + str(e)

    async def handle_appeal(self, ctx: Context[Any], member: discord.Member | discord.User) -> None:

        if isinstance(member, discord.User):
            await ctx.reply("Appeal message not sent. User is not in the server.")
            return None

        time_joined: datetime = member.joined_at if member.joined_at is not None else datetime.now()
        time_since_join = datetime.now() - time_joined

        async with self.database.dao_sessions() as db:
            msgcount: int = await db.msgcount.get_message_count(member.id)

        if time_since_join.days >= 1 or msgcount > 50:
            error = await self.send_appeal_message(member)
            if error: await ctx.reply(error)
            else: await ctx.reply("Appeal message sent.")
        else:
            await ctx.reply(
                "Appeal message not sent. User has not been in the server for 24 hours and/or has not sent 50 messages.")
        return None

    async def log_ban(self, server: discord.Guild, ban: BanData) -> None:

        embed = await self.ban_embed(server, ban)

        channel = server.get_channel(self.config["ch_id"]["#bans-warnings"])
        if channel is None or not isinstance(channel, TextChannel): raise ConfigError("#bans-warnings not correctly set")

        await channel.send(embed=embed)
        return None

    @commands.command()
    @permission_check(Level.STAFF)
    async def ban(self, ctx: Context[Any], *args: str) -> None:

        if not args: return None

        server = await self.require_server(ctx)
        if server is None: return None

        member = await self.user_from_arg(ctx, server, args[0])
        if member is None: return None

        if isinstance(member, discord.Member) and has_permission(member, Level.HELPER):
            await ctx.reply("You cannot ban a staff member.")
            return None

        if len(args) < 2:
            await ctx.reply("Please provide a reason.")
            return None
        reason = args[1]

        if len(args) < 3 or args[2] not in self.flags:
            await ctx.reply("No ban flag found. Please use -nd or -d.")
            return None
        ban_flag = args[2]

        days = 7 if ban_flag == "-d" else 0

        links: tuple[str, ...] = args[3:] if len(args) >= 4 else ()

        try:
            await server.fetch_ban(member)
            await ctx.reply(f"{member.mention} is already banned.")
            return None
        except discord.NotFound:
            pass

        await self.handle_appeal(ctx, member)

        await server.ban(member, reason=reason, delete_message_days=days)

        ban_time = int(round(time() * 1000))
        ban_data = BanData(member.id, ctx.author.id, ban_time, reason, list(links))

        async with self.database.dao_sessions() as db:
            await db.ban.add_ban(ban_data.user, ban_data.banner, ban_data.timestamp, ban_data.reason, ban_data.links)

        await self.log_ban(server, ban_data)

        await ctx.reply(f"User {member.mention} has been banned.")
        return None

    @commands.command(aliases=['bansearch'])
    @permission_check(Level.STAFF)
    async def bans(self, ctx: Context[Any], *args: str) -> None:

        server = await self.require_server(ctx)
        if server is None: return None

        if not args: return None

        user = await self.user_from_arg(ctx, server, args[0])
        if user is None: return None
        user_name = user.display_name

        async with self.database.dao_sessions() as db:
            bans = await db.ban.get_bans(int(args[0]))

        if len(bans) == 0:
            await ctx.reply("**User has no recorded bans.**")
            return None

        for i in range(0, len(bans), 10):
                await ctx.reply(content=f"**{user_name}'s bans**" if i == 0 else None,
                               embeds=await self.bans_embeds(server, bans[i:i+10]))

        return None

    @commands.command()
    @permission_check(Level.STAFF)
    async def unban(self, ctx: Context[Any], *args: str) -> None:

        server = await self.require_server(ctx)
        if server is None: return None

        if not args: return None

        user = await self.user_from_arg(ctx, server, args[0])
        if user is None: return None

        try:
            await server.fetch_ban(user)
        except discord.NotFound:
            await ctx.reply(f"{user.mention} is not banned.")
            return None

        reason = None if len(args) <= 1 else " ".join(args[1:])
        audit_log_reason = f"Unbanned by {ctx.author.display_name} with reason: {reason}"

        await server.unban(user, reason=audit_log_reason)
        await ctx.reply(f"{user.mention} has been unbanned.{f"\nReason: {reason}" if reason is not None else ""}")
        return None

    async def get_ban_message(self, ctx: Context[Any], message_id: int) -> tuple[discord.Message, discord.Embed, datetime, int] | None:
        bans_channel = self.bot.get_channel(self.config["ch_id"]["#bans-warnings"])
        if not isinstance(bans_channel, TextChannel): raise ConfigError("#bans-warnings not correctly set")

        try:
            message = await bans_channel.fetch_message(message_id)
        except discord.NotFound:
            await ctx.reply("Message not found.")
            return None
        except discord.Forbidden:
            await ctx.reply(f"Uh-oh! It looks like I can't access that message.\n"
                            f"Make sure your message is from {bans_channel.mention}")
            return None
        except discord.HTTPException:
            await ctx.reply("Network error.")
            return None

        if len(message.embeds) != 1:
            await ctx.reply("Invalid ban message.")
            return None

        embed = message.embeds[0]
        timestamp = embed.timestamp
        user_id = embed.author.name

        if timestamp is None or user_id is None or not user_id.isdigit():
            await ctx.reply("Invalid ban message.")
            return None

        return message, embed, timestamp, int(user_id)

    @commands.command(aliases=['editban'])
    @permission_check(Level.STAFF)
    async def edit_ban(self, ctx: Context[Any], *args: str) -> None:

        if not args: return None

        server = await self.require_server(ctx)
        if server is None: return None

        if not args[0].isdigit():
            await ctx.reply("Please provide a valid message ID.")
            return None

        if len(args) < 2:
            await ctx.reply("Please provide a valid message ID and updated reason.")
            return None

        ban_info = await self.get_ban_message(ctx, int(args[0]))
        if ban_info is None: return None

        (message, embed, timestamp, user_id) = ban_info

        updated_reason = " ".join(args[1:])
        old_description = embed.description
        embed.description = updated_reason

        try:
            await message.edit(embed=embed)
        except discord.Forbidden:
            await ctx.reply("That message was not sent by me.")
            return None

        async with self.database.dao_sessions() as db:
            result = await db.ban.edit_ban(int(user_id), int(timestamp.timestamp() * 1000), updated_reason)

        if not result:
            await ctx.reply("Database error.")
            embed.description = old_description
            await message.edit(embed=embed)
            return None

        await ctx.reply("Ban reason updated.")
        return None

    @commands.command(aliases=['removeban'])
    async def remove_ban(self, ctx: Context[Any], *args: str) -> None:

        if not args: return None

        if not args[0].isdigit():
            await ctx.reply("Please provide a valid message ID.")

        server = await self.require_server(ctx)
        if not server: return None

        ban_info = await self.get_ban_message(ctx, int(args[0]))
        if ban_info is None: return None

        (message, embed, timestamp, user_id) = ban_info

        async with self.database.dao_sessions() as db:
            result = await db.ban.remove_ban(int(user_id), int(timestamp.timestamp() * 1000))

        if not result:
            await ctx.reply("Given ban not in database.")
            return None

        await message.delete()
        await ctx.reply("Ban deleted.")
        return None


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))

