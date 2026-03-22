import discord

def get_role_ids(roles: discord.member.Member.roles) -> list[int]:
    return [role.id for role in roles]