import discord
import os
import pytz
from discord.ext import commands
from datetime import datetime
from random import randint, choice, sample

from shared.bot_config import PROJECT_PATH, ZOEY_DATA


class StaffCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Aven
    AVEN_USER_ID = 275263004961144833
    AVEN_SLEEP_WINDOW = (2, 8)

    @commands.group(invoke_without_command=True)
    async def aven(self, ctx: commands.Context):
        return await ctx.reply(f"<@{self.AVEN_USER_ID}>, boop!")

    @aven.command(name='time')
    async def aven_time(self, ctx: commands.Context):
        time_uk = datetime.now(pytz.timezone('Europe/London'))
        time_uk_str = time_uk.strftime('%H:%M:%S')
        start, end = self.AVEN_SLEEP_WINDOW
        if end >= time_uk.hour >= start:
            return await ctx.reply(f"The time for Aven is {time_uk_str}. She's probably asleep!")
        return await ctx.reply(f"The time for Aven is {time_uk_str}")


    # Ash
    ASH_IMAGE_PATH = os.path.join(PROJECT_PATH, 'assets/images/ash_staff_command.gif')
    with open(ASH_IMAGE_PATH, 'rb') as f:
        ASH_IMAGE=discord.File(f, filename=ASH_IMAGE_PATH)

    @commands.command()
    async def ash(self, ctx: commands.Context):
        return await ctx.reply(file=self.ASH_IMAGE)


    # Zoey
    @commands.command()
    async def zoey(self, ctx: commands.Context, member: discord.Member = None):
        chosen_obj_1, chosen_obj_2 = sample(ZOEY_DATA.ZOEY_OBJECTS, 2)
        return await ctx.reply(f"Hello{" " + member.display_name if member else ""}, this is Fez from Transpeak's "
                               f"{choice(ZOEY_DATA.ZOEY_JOB_TITLES)}. I'm here to inform you that we have decided to banish "
                               f"you to {choice(ZOEY_DATA.ZOEY_LOCATIONS)}. {choice(ZOEY_DATA.ZOEY_REACTION)} you have a chance at "
                               f"redemption by finding {choice(ZOEY_DATA.ZOEY_STRUCTURES)} and collecting "
                               f"{randint(0,1000)} {chosen_obj_1} and {randint(0,1000)} {chosen_obj_2}. If "
                               f"you fail to do so within {randint(1,7)} days we will have no choice but to report "
                               f"you for {choice(ZOEY_DATA.ZOEY_CRIME)}. Thank you for your time.")


async def setup(bot):
    await bot.add_cog(StaffCommands(bot))