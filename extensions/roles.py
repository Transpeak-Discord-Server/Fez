from typing import Any

import discord
from discord.ext import commands

from shared.utils.misc import get_member_or_user, require_server
from shared.utils.permissions import permission_check, Level

from shared.config import Config

rl_id = Config.json_config['rl_id']
reg_rl_id = Config.json_config['reg_rl_id']

class Roles(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @permission_check(Level.HELPER)
    @commands.command(aliases=['addroles'])
    async def add_roles(self, ctx: commands.Context[Any], *args: str) -> None:

        server = await require_server(ctx)
        if not server:
            return None

        if not args:
            await ctx.reply("Usage: !addroles [userid] [list of roles, separated by spaces]")
            return None

        if len(args) < 2:
            await ctx.reply("Please include both the user ID and the list of roles to add.")

        if not args[0].isdigit():
            await ctx.reply("Please include the user ID of the user to add the roles to.")
            return None

        user = await get_member_or_user(server, self.bot, int(args[0]))
        if user is None:
            await ctx.reply("User not found.")
            return None
        if isinstance(user, discord.User):
            await ctx.reply("User is not on the server")
            return None

        role_names = args[1:]

        roles_to_add: list[discord.Role] = []
        unknown_roles: list[str] = []

        for role_name in role_names:
            if role_name not in reg_rl_id:
                unknown_roles.append(role_name)
                continue
            role = server.get_role(reg_rl_id[role_name])
            if role is None:
                unknown_roles.append(role_name)
                continue
            roles_to_add.append(role)

        await user.add_roles(*roles_to_add)
        unkwn_rls_str = f" (Could not add roles: {", ".join(unknown_roles)})" if len(unknown_roles) > 0 else ""
        await ctx.reply(f"Roles added to user.{unkwn_rls_str}")

        return None