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

import discord
from discord import app_commands

from shared.transpeak_bot import TranspeakBot
from shared.utils.permissions import permission_check, Level

@app_commands.command()
@permission_check(Level.STAFF)
async def mentionfind(interaction: discord.Interaction[TranspeakBot], search_term: str) -> None:
    query = search_term.strip().lower()
    results = ['{} {}#{}'.format(x.mention, x.name if x.nick is None else f'{x.nick} *aka {x.name}*', x.discriminator) for x in interaction.guild.members if query in (x.name+'\u200b'+x.display_name+'\u200b'+x.discriminator).lower()]

    if not results:
        await interaction.response.send_message("No results found", ephemeral=True)
        return

    elif len(results) > 50:
        await interaction.response.send_message(f"That query returned **{len(results)}** results. Please try a more specific query.", ephemeral=True)
        return

    else:
        try:
            await interaction.response.send_message(f"**Search results ({len(results)}):**\n{"\n".join(results)}")

        except Exception as e:
            if "too long" in str(e):
                await interaction.response.send_message("Too many results.", ephemeral=True)

            else:
                print(e)
                await interaction.response.send_message("An error occured", ephemeral=True)


async def setup(bot: TranspeakBot) -> None:
    bot.tree.add_command(mentionfind)