from datetime import datetime
from time import time
from typing import Any

from discord.ext.commands import Context

import discord
from discord.ext import commands

from shared.config import Config
from shared.database.old_db.database import OldDatabase
from shared.utils.permissions import permission_check, Level, has_permission

class Ban(commands.Cog):

    flags = ["-nd", "-d"]
    config = Config.json_config

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = OldDatabase()

    def get_ban_flag(self, reason: tuple[str, ...]) -> str | None:
        for flag in reason:
            if flag in self.flags:
                return flag
        return None

    @classmethod
    async def send_appeal_message(cls, member: discord.Member) -> None | str:
        try:
            await member.send(cls.config["APPEAL_MESSAGE"])
            return None
        except discord.Forbidden as e:
            return "Could not send appeal message. Reason: " + str(e)
        except discord.HTTPException as e:
            return "Could not send appeal message. Reason: " + str(e)

    async def handle_appeal(self, ctx: Context[Any], member: discord.Member) -> None:

        time_joined: datetime = member.joined_at if member.joined_at is not None else datetime.now()
        time_since_join = datetime.now() - time_joined

        async with self.database.dao_sessions() as db:
            msgcount: int = await db.msgcount.get_message_count(member.id)

        if time_since_join.days > 1 and msgcount > 50:
            error = await self.send_appeal_message(member)
            if error:
                await ctx.send(error)
        else:
            await ctx.send(
                "Appeal message not sent. User has not been in the server for 24 hours and/or has not sent 50 messages.")

    @commands.command()
    @permission_check(Level.STAFF)
    async def ban(self, ctx: Context[Any], *args: str) -> None:
        if not args: return None

        server = ctx.guild
        if server is None:
            await ctx.send("This command can only be used within Transpeak.")
            return None

        if not args[0].isdigit():
            await ctx.send("Please provide a valid user ID.")
            return None

        member = server.get_member(int(args[0]))

        if not member:
            await ctx.send("User not found.")
            return None

        if has_permission(member, Level.HELPER):
            await ctx.send("You cannot ban a staff member.")
            return None

        reason = " ".join(args[1:])
        if not reason:
            await ctx.send("Please provide a reason.")
            return None

        ban_flag = self.get_ban_flag(args[1:])
        if not ban_flag:
            await ctx.send("No ban flag found. Please use -nd or -d.")
            return None

        reason = " ".join(reason)
        reason = reason.replace(ban_flag, "", 1)

        days = 0
        if ban_flag == "-d":
            days = 7

        if isinstance(member, discord.Member):
            await self.handle_appeal(ctx, member)

        await server.ban(member, reason=reason, delete_message_days=days)

        async with self.database.dao_sessions() as db:
            await db.ban.add_ban(member.id, ctx.author.id, int(round(time() * 1000)), reason)

        await ctx.send(f"User {member.mention} has been banned.")
        return None

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ban(bot))

