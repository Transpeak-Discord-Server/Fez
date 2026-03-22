from functools import singledispatch

import discord
from datetime import datetime

def get_role_ids(roles: discord.member.Member.roles):
    return [role.id for role in roles]


# format time

@singledispatch
def format_time(time, time_format: str = "t") -> str:
    return f"<t:{int(time)}:{time_format}>"

@format_time.register(datetime)
def _(time: datetime, time_format: str = "t") -> str:
    return format_time(int(time.timestamp()), time_format)