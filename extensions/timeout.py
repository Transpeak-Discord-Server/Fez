from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from shared.config import Config
from shared.utils.misc import require_server
from shared.utils.permissions import permission_check, Level

config = Config.json_config

timeout_category_id: int = config['cat_id']['timeout']
timeout_role_id: int = config['rl_id']['timeout']

timeout_msg: str


async def add_timeout(user: discord.Member, server: discord.Guild, interaction: discord.Interaction[commands.Bot]) -> None:
    timeout_channel_name = f'timeout-{user.id}'
    timeout_role = server.get_role(timeout_role_id)
    timeout_category = server.get_channel(timeout_category_id)

    if not timeout_role:
        raise ValueError("Could not get timeout role from config ID")
    if not isinstance(timeout_category, discord.CategoryChannel):
        raise ValueError("Could not get timeout category from config ID")

    bot_role = server.get_role(config['rl_id']['/'])
    lead_mod_role = server.get_role(config['rl_id']['+'])
    mod_role = server.get_role(config['rl_id']['-'])
    staff_role = server.get_role(config['rl_id']['staff'])
    helper_role = server.get_role(config['rl_id']['helper'])

    if bot_role is None or lead_mod_role is None or mod_role is None or staff_role is None or helper_role is None:
        raise ValueError("Could not find one or more roles from config IDs")

    channel_overwrites: dict[discord.Role | discord.Member | discord.Object, discord.PermissionOverwrite] = {
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        bot_role: discord.PermissionOverwrite(view_channel=True,send_messages=True,manage_channels=True),
        lead_mod_role: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True),
        mod_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        staff_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        helper_role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }

    channel = await server.create_text_channel(
        timeout_channel_name,
        category=timeout_category,
        overwrites=channel_overwrites,
        reason=f"Timeout channel for {user.display_name}, timed out by: {interaction.user.display_name} ({interaction.user.id}"
    )

    # TODO: save roles when get_database() is merged into main

    await user.remove_roles(*user.roles, reason=f"Role removal for timeout by: {interaction.user.display_name} ({interaction.user.id})")
    await user.add_roles(timeout_role, reason=f"Timed out by: {interaction.user.display_name} ({interaction.user.id})")
    await channel.send(timeout_msg)

@app_commands.command()
@permission_check(Level.HELPER)
async def timeout(interaction: discord.Interaction[commands.Bot], user: discord.Member) -> None:
    server = await require_server(interaction)
    if not server: return

    timeout_role = server.get_role(timeout_role_id)
    timeout_channel_name = f'timeout-{user.id}'

    # User is not timed out yet
    if user.get_role(timeout_role_id) is None:
        await add_timeout(user, server, interaction)
        await interaction.response.send_message(f"{user.display_name} is now in timeout.")
    # User is already timed out



async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(timeout)

    global timeout_msg
    with open(Path(Path.cwd() / ".." / "shared" / "messages" / "timeout")) as file:
        timeout_msg = file.read()