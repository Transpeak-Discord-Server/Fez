import discord
from discord.ext import commands

class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def timeout(self, ctx, args: str):
        user = ctx.guild.get_member(args)

        if user is None:
            return await ctx.send() # Switch out with reply once you've gotten it to work & the file is set up

async def setup(bot):
    await bot.add_cog(Timeout(bot))