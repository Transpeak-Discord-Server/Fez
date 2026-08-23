from typing import Any

import discord
import os
import pytz
from discord.ext import commands
from datetime import datetime
from random import randint, choice, sample
from pathlib import Path

from discord.ext.commands import Context

from shared.config import Config

PROJECT_PATH = Path(os.path.dirname(__file__)).parent.parent

class StaffCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def cog_check(self, ctx: Context[Any]) -> bool:
        return ctx.guild is not None

    # Aven
    AVEN_USER_ID = 275263004961144833
    AVEN_SLEEP_WINDOW = (2, 8)

    @commands.group(invoke_without_command=True)
    async def aven(self, ctx: commands.Context[Any]) -> None:
        await ctx.reply(f"<@{self.AVEN_USER_ID}>, boop!")
        return None

    @aven.command(name='time') # type: ignore
    async def aven_time(self, ctx: commands.Context[Any]) -> None:
        time_uk = datetime.now(pytz.timezone('Europe/London'))
        time_uk_str = time_uk.strftime('%H:%M:%S')
        start, end = self.AVEN_SLEEP_WINDOW
        if end >= time_uk.hour >= start:
            await ctx.reply(f"The time for Aven is {time_uk_str}. She's probably asleep!")
            return None
        await ctx.reply(f"The time for Aven is {time_uk_str}")
        return None


    # Ash
    ASH_IMAGE_PATH = os.path.join(PROJECT_PATH, 'private/images/ash_staff_command.gif')

    @commands.command()
    async def ash(self, ctx: commands.Context[Any]) -> None:
        with open(self.ASH_IMAGE_PATH, 'rb') as f:
            await ctx.reply(file=discord.File(f, self.ASH_IMAGE_PATH))
        return None

    # Zoey
    ZOEY_DATA = Config.json_config['ZOEY_DATA']

    @commands.command()
    async def zoey(self, ctx: commands.Context[Any], member_str: str | None = None) -> None:
        member_int = int(member_str) if member_str and member_str.isdigit() else None

        server = ctx.guild
        if not server: return None

        member = server.get_member(member_int) if member_int else None
        chosen_obj_1, chosen_obj_2 = sample(self.ZOEY_DATA['ZOEY_OBJECTS'], 2)

        await ctx.reply(f"Hello{" " + member.display_name if member else ""}, this is Fez from Transpeak's "
           f"{choice(self.ZOEY_DATA['ZOEY_JOB_TITLES'])}. I'm here to inform you that we have decided to banish "
           f"you to {choice(self.ZOEY_DATA['ZOEY_LOCATIONS'])}. {choice(self.ZOEY_DATA['ZOEY_REACTION'])} you have a chance at "
           f"redemption by finding {choice(self.ZOEY_DATA['ZOEY_STRUCTURES'])} and collecting "
           f"{randint(0,1000)} {chosen_obj_1} and {randint(0,1000)} {chosen_obj_2}. If "
           f"you fail to do so within {randint(1,7)} days we will have no choice but to report "
           f"you for {choice(self.ZOEY_DATA['ZOEY_CRIME'])}. Thank you for your time.")
        return None

    # Cat
    CAT_IMAGE_PATH = os.path.join(PROJECT_PATH, 'private/images/night.gif')

    @commands.command()
    async def cat(self, ctx: commands.Context[Any]) -> None:
        with open(self.CAT_IMAGE_PATH, 'rb') as f:
            await ctx.reply(file=discord.File(f, 'night_staff_command.gif'))
        return None

    # Luna
    LUNA_IMAGE_PATH = os.path.join(PROJECT_PATH, 'private/images/luna_staff_command.png')

    @commands.command()
    async def luna(self, ctx: commands.Context[Any]) -> None:
        with open(self.LUNA_IMAGE_PATH, 'rb') as f:
            await ctx.reply(file=discord.File(f, 'luna_staff_command.png'))
        return None

    # Simon
    SIMON_USER_ID = 1383285080700747837

    @commands.command()
    async def simon(self, ctx: commands.Context[Any]) -> None:
        await ctx.reply(f"<@{self.SIMON_USER_ID}> awoo!")
        return None

    # Ren
    @commands.command()
    async def ren(self, ctx: commands.Context[Any]) -> None:
        await ctx.reply("yo")
        return None

    # Crymson
    CRYMSON_IMAGE_PATH = os.path.join(PROJECT_PATH, 'private/images/frank-iero-six-seven.gif')

    @commands.command()
    async def crymson(self, ctx: commands.Context[Any]) -> None:
        with open(self.CRYMSON_IMAGE_PATH, 'rb') as f:
            await ctx.reply(file=discord.File(f, 'crymson_staff_command.gif'))
        return None

    # Katelyn
    KATELYN_IMAGE_PATH = os.path.join(PROJECT_PATH, 'private/images/katelyn.gif')

    @commands.command()
    async def katelyn(self, ctx: commands.Context[Any]) -> None:
        with open(self.KATELYN_IMAGE_PATH, 'rb') as f:
            await ctx.reply(file=discord.File(f, 'katelyn_staff_command.gif'))
        return None

    # Icarus
    ICARUS_IMAGE_PATH = os.path.join(PROJECT_PATH, 'private/images/icarus.gif')

    @commands.command()
    async def icarus(self, ctx: commands.Context[Any]) -> None:
        with open(self.ICARUS_IMAGE_PATH, 'rb') as f:
            await ctx.reply(file=discord.File(f, 'icarus_staff_command.gif'))
        return None


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StaffCommands(bot))
    return None