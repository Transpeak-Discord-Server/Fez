import discord, sqlite3, os, sys

from datetime import datetime
from time import time

from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MemberNotFound

from shared.utils.permissions import permission_check, Level, has_permission
# from shared.utils.misc import getsavedroles, saveroles, is_booster, get_member_or_user, format_time
from shared.config import Config
from shared.database.old_db.database import OldDatabase

# rl_id = Config.json_config['rl_id']
# identities_for_cmd = Config.json_config["identities_for_cmd"]

class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = OldDatabase()
        self.config = Config.json_config

    @commands.command()
    async def timeout(self, ctx, member: discord.Member):      
        rl_id = self.config["rl_id"]
        print(rl_id)
    
    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, MemberNotFound):
            return await ctx.reply("No member found with that ID.")
        
        elif isinstance(error, MissingRequiredArgument):
            return await ctx.reply("Please provide a user ID.")

async def setup(bot):
    await bot.add_cog(Timeout(bot))