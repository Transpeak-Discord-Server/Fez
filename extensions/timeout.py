import discord
from discord import app_commands
from discord.ext import commands

from shared.config import Config
from shared.utils.misc import require_server
from shared.utils.permissions import permission_check, Level

config = Config.json_config

timeout_role_id: int = config['rl_id']['timeout']
_timeout_role: discord.Role | None = None

def get_timeout_role(server: discord.Guild) -> discord.Role:
    if _timeout_role is not None: return _timeout_role
    role = server.get_role(timeout_role_id)
    if not role:
        raise ValueError("Could not find timeout role from config id")
    return role

@app_commands.command()
@permission_check(Level.HELPER)
async def timeout(interaction: discord.Interaction[commands.Bot], user: discord.Member) -> None:
    server = await require_server(interaction)
    if not server: return

    timeout_role = get_timeout_role(server)


async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(timeout)