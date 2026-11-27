# Fez/TransBot - A Discord.py bot for Transpeak
# Copyright (C) 2026 Fez project contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import discord.abc
from discord import app_commands

from shared.transpeak_bot import TranspeakBot
from shared.utils.permissions import permission_check, Level

@app_commands.command()
@permission_check(Level.ADMIN)
async def speak(interaction: discord.Interaction[TranspeakBot], channel: discord.TextChannel | discord.VoiceChannel | discord.Thread, message: str) -> None:
    try:
        await channel.send(message)
    except (discord.NotFound, discord.Forbidden) as e:
        await interaction.response.send_message("I cannot send a message to that channel.", ephemeral=True)
        return
    await interaction.response.send_message(f"Sent message to {channel.mention}", ephemeral=True)

async def setup(bot: TranspeakBot) -> None:
    bot.tree.add_command(speak)