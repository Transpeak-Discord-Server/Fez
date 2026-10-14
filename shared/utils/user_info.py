import discord

_wl_users = []

def is_on_wl(user: discord.User | discord.Member) -> bool:
    if user.id in _wl_users:
        return True
    return False