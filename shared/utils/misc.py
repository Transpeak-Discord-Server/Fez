from functools import singledispatch
from datetime import datetime
from typing import Iterable, Protocol, Any

import discord
from discord import Member, User
from discord.ext import commands

from shared.utils.permissions import UserPermissionsError, Level

def __init__():
    pass

class HasId(Protocol):
    id: int

def get_ids(items: Iterable[HasId]) -> list[int]:
    return [item.id for item in items]

def get_week() -> int:
    a = datetime(2017, 7, 31, 00, 00, 00)
    b = datetime.now()
    return int((b - a).total_seconds() / (7 * 24 * 60 * 60))

async def get_member_or_user(server: discord.Guild, bot: discord.Client, user_id: int) -> Member | User | None:
    try:
        return server.get_member(user_id) or await server.fetch_member(user_id)
    except discord.NotFound: pass
    try:
        return bot.get_user(user_id) or await bot.fetch_user(user_id)
    except discord.NotFound:
        return None

# format time

@singledispatch
def format_time(time: Any, time_format: str = "t") -> str:
    return f"<t:{int(time)}:{time_format}>"

@format_time.register(datetime)
def _(time: datetime, time_format: str = "t") -> str:
    return format_time(int(time.timestamp()), time_format)

# Handle error

async def shared_error(ctx: commands.Context[Any], error: Exception):
    if isinstance(error, commands.CommandNotFound):
        return None
    if isinstance(error, UserPermissionsError):
        if error.required_perms == Level.REGISTERED:
            await ctx.reply("You need to be registered to do that! Please ping a staff member for help.")
            return None
        await ctx.reply(f"You need to be a {error.required_perms} to do that!")
        return None
    print(error)
    return None