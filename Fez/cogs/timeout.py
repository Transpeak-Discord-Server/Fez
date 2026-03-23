import discord
from discord.ext import commands
from shared.utils.permissions import permission_check, Level, has_permission
from shared.utils.misc import getsavedroles
from shared.bot_config import rl_id
from discord.ext.commands import MissingRequiredArgument, MemberNotFound

class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def timeout(self, ctx, member: discord.Member):      
        if any(role in [rl_id["staff"], rl_id["bot"], rl_id["staff-junior"]] for role in ctx.author.roles) or (rl_id["helper"] in member.roles and rl_id["helper"] in ctx.author.roles):
            return await ctx.reply("No")
        
        timeout_id = 332937538648014848

        if ctx.guild.get_role(timeout_id) in member.roles:
            og_roles = await getsavedroles(member.roles)
        
        await getsavedroles(member.roles)
    
    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            return await ctx.reply("No member found with that ID.")
        
        elif isinstance(error, MissingRequiredArgument):
            return await ctx.reply("Please provide a user ID.")

async def setup(bot):
    await bot.add_cog(Timeout(bot))