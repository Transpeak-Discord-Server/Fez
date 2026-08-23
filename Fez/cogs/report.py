from typing import Any

import discord
from discord import app_commands, ForumChannel, DMChannel, PartialMessageable
from discord.ext import commands
from discord.ext.commands import Context

from shared.config import Config

config = Config.json_config

class ReportForm(discord.ui.Modal, title="Report Message"):

    reports_channel: ForumChannel
    reports_over18_channel: ForumChannel

    @classmethod
    async def ready(cls, bot: commands.Bot) -> None:
        reports_channel = await bot.fetch_channel(config['ch_id']['reports'])
        if not isinstance(reports_channel, ForumChannel):
            raise ValueError("reports channel is not a forum channel")
        cls.reports_channel = reports_channel

        reports_over18_channel = await bot.fetch_channel(config['ch_id']['reports-over18'])
        if not isinstance(reports_over18_channel, ForumChannel):
            raise ValueError("reports-over18 channel is not a forum channel")
        cls.reports_over18_channel = reports_over18_channel

    extra_details: discord.ui.TextInput[Any] = discord.ui.TextInput(
        label="Extra Details",
        style=discord.TextStyle.paragraph
    )
    over_18: discord.ui.TextInput[Any] = discord.ui.TextInput(
        label="Does this incident contain adult content?",
        placeholder="Enter only \"Yes\" or leave blank",
        required=False
    )

    def __init__(self, message: discord.Message):
        super().__init__()
        self.message = message
        if message.guild is None: raise RuntimeError("No guild for reported message")
        self.staff_alert = message.guild.get_role(config['rl_id']['staff-alert'])

    async def on_submit(self, interaction: discord.Interaction) -> None:

        report_channel = self.reports_over18_channel if self.over_18.value.lower() == "yes" else self.reports_channel

        if isinstance(self.message.channel, DMChannel | PartialMessageable): return None

        thread = await report_channel.create_thread(
            name=f"@{self.message.author.name} in #{self.message.channel.name}",
            content=f"{self.message.content}"
        )

        await thread.thread.send(
            f":arrow_right: {self.message.jump_url}\n"
            f"### Extra Details:\n"
            f"{self.extra_details.value}\n"
            f"### Report made by:\n"
            f"* {interaction.user.mention}\n"
            f"* `{interaction.user.id}`\n"
            f"### Reported user:\n"
            f"* {self.message.author.mention}\n"
            f"* `{self.message.author.id}`\n"
            f"{self.staff_alert.mention if self.staff_alert is not None else ''}"
        )

        await interaction.response.send_message("Report submitted! Staff may reach out if they need further information.", ephemeral=True)
        return None

async def report_message(interaction: discord.Interaction, message: discord.Message) -> None:

    server = interaction.guild
    if not server: return None

    await interaction.response.send_modal(ReportForm(message))
    return None

report_button = app_commands.ContextMenu(
        name="Report Message",
        callback=report_message
    )

class Report(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.tree.add_command(report_button)

    async def cog_load(self) -> None:
        await ReportForm.ready(self.bot)
        await self.bot.tree.sync()

    def cog_check(self, ctx: Context[Any]) -> bool:
        return ctx.guild is not None

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Report(bot))
    return None