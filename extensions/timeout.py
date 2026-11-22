import os
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands

from shared.config import Config
from shared.database.RoleDAO import RoleDAO
from shared.database.__main__ import get_database
from shared.utils.misc import require_server
from shared.utils.permissions import permission_check, Level

config = Config.json_config
database = get_database()

timeout_category_id: int = config['cat_id']['timeouts']
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
        server.default_role: discord.PermissionOverwrite(view_channel=False),
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

    roles_to_remove = [role for role in user.roles
                       if not role.is_default() and
                       role.name not in config['identities']['transfemale_pronouns'] and
                       role.name not in config['identities']['transmale_pronouns'] and
                       role.name not in config['identities']['nonbinary_pronouns']]

    async with database.get_session() as session:
        role_dao = RoleDAO(session)
        await role_dao.save_roles(user.id, roles_to_remove)

    await user.remove_roles(*roles_to_remove, reason=f"Role removal for timeout by: {interaction.user.display_name} ({interaction.user.id})")
    await user.add_roles(timeout_role, reason=f"Timed out by: {interaction.user.display_name} ({interaction.user.id})")
    await channel.send(f"{user.mention} {timeout_msg}")
    await interaction.followup.send(f"{user.display_name} is now in timeout.")

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

    await user.remove_roles(timeout_role, reason=f"Removed from timeout by {interaction.user.display_name} ({interaction.user.id})")

    async with database.get_session() as session:
        role_dao = RoleDAO(session)
        await user.add_roles(*(await role_dao.get_saved_roles(user.id, server)), reason=f'Restoring roles from before timeout')

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

    await timeout_channel.edit(name=f'closed-{user.id}', reason=f'Timeout removed by {interaction.user.display_name} ({interaction.user.id})')
    await timeout_channel.send(f"{staff_alert_role.mention}, this timeout has concluded.")
    await interaction.followup.send(f"{user.display_name} has been removed from timeout and roles have been restored.")



@app_commands.command()
@permission_check(Level.HELPER)
async def timeout(interaction: discord.Interaction[commands.Bot], user: discord.Member) -> None:
    server = await require_server(interaction)
    if not server: return

    # This command can take a while, so let Discord know we got it and are working on it
    await interaction.response.defer(thinking=True)

    # User is not timed out yet
    if user.get_role(timeout_role_id) is None:
        await add_timeout(user, server, interaction)
    # User is already timed out
    else:
        await remove_timeout(user, server, interaction)



async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(timeout)

    global timeout_msg
    file_path = Path(os.path.dirname(__file__))
    with open(Path(file_path / ".." / "shared" / "messages" / "timeout")) as file:
        timeout_msg = file.read()