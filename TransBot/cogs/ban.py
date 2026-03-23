import os
from datetime import datetime
from time import time
from shared.database.msgcount_manager import MsgCountManager
from shared.database.ban_manager import BanManager

import discord
from discord.ext import commands

from shared.utils.permissions import permission_check, Level, has_permission
import json
with open(os.path.join(os.path.dirname(__file__), '../../shared/bot_config.json')) as f:
    config = json.load(f)

class Ban(commands.Cog):

    flags = ["-nd", "-d"]

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.msgcount_manager = None
        self.ban_manager = None

    async def cog_load(self):
        self.msgcount_manager = await MsgCountManager().initialise()
        self.ban_manager = await BanManager().initialise()

    def get_ban_flag(self, reason: tuple[str, ...]) -> str | None:
        for flag in reason:
            if flag in self.flags:
                return flag
        return None

    @staticmethod
    async def send_appeal_message(member: discord.Member):
        try:
            await member.send(config["APPEAL_MESSAGE"])
            return None
        except discord.Forbidden as e:
            return "Could not send appeal message. Reason: " + str(e)
        except discord.HTTPException as e:
            return "Could not send appeal message. Reason: " + str(e)

    async def handle_appeal(self, ctx, member: discord.Member):
        time_since_join = datetime.now() - member.joined_at
        if time_since_join.days > 1 and await self.msgcount_manager.get_msg_count(member.id) > 50:
            error = await self.send_appeal_message(member)
            if error:
                await ctx.send(error)
        else:
            await ctx.send(
                "Appeal message not sent. User has not been in the server for 24 hours and/or has not sent 50 messages.")

    @commands.command()
    @permission_check(Level.STAFF)
    async def ban(self, ctx, *args: str):
        if not args: return None

        if not args[0].isdigit():
            return await ctx.send("Please provide a valid user ID.")

        member = ctx.guild.get_member(int(args[0])) if ctx.guild.get_member(int(args[0])) else self.bot.get_user(int(args[0]))
        _is_member = isinstance(member, discord.Member)
        if not member:
            return await ctx.send("User not found.")

        if _is_member and has_permission(member, Level.HELPER):
            return await ctx.send("You cannot ban a staff member.")

        reason = args[1:]
        if not reason:
            return await ctx.send("Please provide a reason.")

        ban_flag = self.get_ban_flag(reason)
        if not ban_flag:
            return await ctx.send("No ban flag found. Please use -nd or -d.")

        reason = " ".join(reason)
        reason = reason.replace(ban_flag, "", 1)

        days = 0
        if ban_flag == "-d":
            days = 14

        if _is_member:
            await self.handle_appeal(ctx, member)

        await ctx.guild.ban(member, reason=reason, delete_message_days=days)

        await self.ban_manager.add_ban(member.id, ctx.author.id, int(round(time() * 1000)), reason)
        return await ctx.send(f"User {member.mention} has been banned.")



async def setup(bot):
    await bot.add_cog(Ban(bot))

