import discord
from discord.ext import commands
from shared.utils.permissions import permission_check, Level, has_permission
from shared.utils.misc import getsavedroles
from shared.bot_config import rl_id

class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def timeout(self, ctx, args: str):
        user = ctx.guild.get_member(args)

        if user is None:
            return await ctx.reply("No member found with that ID.")
        
        if any(role in [rl_id["staff"], rl_id["bot"], rl_id["staff-junior"]] for role in ctx.author.roles):
            return await ctx.reply("No")
        
        timeout_id = 332937538648014848

        if discord.utils.get(ctx.guild.roles(), id = timeout_id) in user.roles():
            getsavedroles("")

async def setup(bot):
    await bot.add_cog(Timeout(bot))