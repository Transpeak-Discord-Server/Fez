import discord.abc
from discord import app_commands
from discord.ext import commands

from shared.utils.permissions import permission_check, Level


@app_commands.command()
@permission_check(Level.ADMIN)
async def speak(interaction: discord.Interaction[commands.Bot], channel: discord.TextChannel | discord.VoiceChannel | discord.Thread, message: str, reply_to: discord.Message | None) -> None:
    try:
        if reply_to:
            await reply_to.reply(message)
        else:
            await channel.send(message)
    except (discord.NotFound, discord.Forbidden) as e:
        await interaction.response.send_message("I cannot send a message to that channel.", ephemeral=True)
        return
    await interaction.response.send_message(f"Sent message to {channel.mention}", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(speak)