import discord

def get_role_ids(roles: discord.member.Member.roles):
    return [role.id for role in roles]