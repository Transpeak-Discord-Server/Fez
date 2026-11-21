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
    await interaction.response.send_message(f"{user.display_name} is now in timeout.")

def find_timeout_channel(user: discord.Member, server: discord.Guild) -> discord.TextChannel | None:
    timeout_channel_name = f'timeout-{user.id}'
    timeout_category = server.get_channel(timeout_category_id)
    if not isinstance(timeout_category, discord.CategoryChannel):
        raise ValueError("Could not get timeout category from config ID")

    timeout_channels = timeout_category.channels
    for channel in timeout_channels:
        if isinstance(channel, discord.TextChannel) and channel.name == timeout_channel_name:
            return channel
    return None

async def remove_timeout(user: discord.Member, server: discord.Guild, interaction: discord.Interaction[commands.Bot]) -> None:
    timeout_role = server.get_role(timeout_role_id)
    if not timeout_role:
        raise ValueError("Could not get timeout role from config ID")

    timeout_channel = find_timeout_channel(user, server)
    if not timeout_channel:
        await interaction.response.send_message("Could not find user's timeout channel.")
        return

    await user.remove_roles(timeout_role)

    # TODO: get roles and add them back once get_database() is in main

    lead_mod_role = server.get_role(config['rl_id']['+'])
    mod_role = server.get_role(config['rl_id']['-'])
    staff_role = server.get_role(config['rl_id']['staff'])
    helper_role = server.get_role(config['rl_id']['helper'])
    staff_alert_role = server.get_role(config['rl_id']['staff-alert'])

    if lead_mod_role is None or mod_role is None or staff_role is None or helper_role is None or staff_alert_role is None:
        raise ValueError("Could not find one or more roles from config IDs")

    await timeout_channel.set_permissions(user, overwrite=None)
    await timeout_channel.set_permissions(lead_mod_role, overwrite=discord.PermissionOverwrite(view_channel=True,send_messages=False))
    await timeout_channel.set_permissions(mod_role, overwrite=None)
    await timeout_channel.set_permissions(staff_role, overwrite=None)
    await timeout_channel.set_permissions(helper_role, overwrite=None)

    await timeout_channel.send(f"{staff_alert_role.mention}, this timeout has concluded.")
    await interaction.response.send_message(f"{user.display_name} has been removed from timeout and roles have been restored.")



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
    # User is already timed out
    else:
        await remove_timeout(user, server, interaction)



async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(timeout)

    global timeout_msg
    with open(Path(Path.cwd() / ".." / "shared" / "messages" / "timeout")) as file:
        timeout_msg = file.read()