import discord
from discord.ext import commands
from datetime import datetime

class StaffCommands(commands.Cog):

    aven_userid: int = 275263004961144833

    @commands.command()
    async def aven(self, ctx: commands.Context, args: str):
        if args == 'time':
            time_uk = datetime.now('Europe/London')
            time_uk_str = time_uk.strftime('%H:%M:%S')
            if 9 > time_uk > 1:
                return await ctx.reply(f"The time for Aven is {time_uk_str}. She's probably asleep!")
            return await ctx.reply(f"The time for Aven is {time_uk_str}")
        return await ctx.reply(f"<@{aven_userid}>, boop!")

def setup(bot):
    bot.add_cog(StaffCommands(bot))