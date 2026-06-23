from datetime import datetime
from time import time
from typing import Any

import discord
from discord.ext import commands
from discord.ext.commands import Context

from shared.config import Config
from shared.database.data import BanData
from shared.database.old_db.database import OldDatabase
from shared.utils.misc import get_member_or_user, format_time
from shared.utils.permissions import permission_check, Level, has_permission


class Ban(commands.Cog):

    flags = ["-nd", "-d"]
    config = Config.json_config

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = OldDatabase()

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

    @commands.command()
    @permission_check(Level.STAFF)
    async def ban(self, ctx: Context[Any], *args: str) -> None:

        server = ctx.guild
        if server is None:
            await ctx.reply("This command can only be used within Transpeak.")
            return None

        if not args or not args[0].isdigit():
            await ctx.reply("Please provide a valid user ID.")
            return None

        member = await get_member_or_user(server, self.bot, int(args[0]))

        if not member:
            await ctx.reply("User not found.")
            return None

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

        await self.handle_appeal(ctx, member)

        await server.ban(member, reason=reason, delete_message_days=days)

        async with self.database.dao_sessions() as db:
            await db.ban.add_ban(member.id, ctx.author.id, int(round(time() * 1000)), reason, list(links))

        await ctx.reply(f"User {member.mention} has been banned.")
        return None

    async def bans_embeds(self, server: discord.Guild, bans: list[BanData]) -> list[discord.Embed]:

        embeds: list[discord.Embed] = []

        for ban in bans:

            banned_by = await get_member_or_user(server, self.bot, ban.banner)
            banner_name = banned_by.display_name if banned_by else "Unknown"
            banner_icon = banned_by.display_avatar.url if banned_by else None

            timestamp = format_time(ban.timestamp//1000, "f")
            embed = discord.Embed(
                description=ban.reason,
                color=discord.Color.red()
            )
            embed.set_author(name=banner_name, icon_url=banner_icon)
            if len(ban.links) > 0: embed.add_field(name="Links", value="\n".join(ban.links))
            embed.add_field(name="Timestamp", value=timestamp)

            embeds.append(embed)

        return embeds

    @commands.command(aliases=['bansearch'])
    @permission_check(Level.STAFF)
    async def bans(self, ctx: Context[Any], *args: str) -> None:

        server = ctx.guild
        if server is None:
            await ctx.reply("This command can only be used within Transpeak.")
            return None

        if not args: return None

        if not args[0].isdigit():
            await ctx.reply("Please provide a valid user ID.")
            return None

        user = await get_member_or_user(server, self.bot, int(args[0]))
        user_name = user.display_name if user is not None else args[0]

        async with self.database.dao_sessions() as db:
            bans = await db.ban.get_bans(int(args[0]))

        if len(bans) == 0:
            await ctx.reply("**User has no recorded bans.**")
            return None

        for i in range(0, len(bans), 10):
                await ctx.reply(content=f"**{user_name}'s bans**" if i == 0 else None,
                               embeds=await self.bans_embeds(server, bans[i:i+10]))

        return None

    async def unban(self, ctx: Context[Any], *args: str) -> None:

        server = ctx.guild
        if server is None:
            await ctx.reply("This command can only be used within Transpeak.")
            return None

        if not args: return None

        if not args[0].isdigit():
            await ctx.reply("Please provide a valid user ID.")
            return None

        user = await get_member_or_user(server, self.bot, int(args[0]))
        if user is None:
            await ctx.reply("User not found.")
            return None

        try:
            await server.fetch_ban(user)
        except discord.NotFound:
            await ctx.reply(f"{user.display_name} is not banned.")
            return None

        reason = "" if len(args) <= 1 else " ".join(args[1:])

        await server.unban(user, reason=reason)
        await ctx.reply(f"{user.display_name} has been unbanned.")
        return None

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))

