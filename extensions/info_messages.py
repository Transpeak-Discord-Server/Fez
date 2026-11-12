import dataclasses
import json
import os
from pathlib import Path
from typing import List

import discord
from discord import app_commands
from discord.ext import commands

from shared.utils.misc import send_split_message
from shared.utils.permissions import permission_check, Level
from shared.config import Config

project_path = Path(os.path.dirname(__file__)).parent
messages_path = project_path / "shared" / "messages"
default_file_name = messages_path / "default.json"


@dataclasses.dataclass
class MessageGroup:
    file_name: str
    channel: discord.TextChannel
    messages: List[str]
    clear_channel: bool


class InfoMessages(app_commands.Group):

    loaded_files: List[Path]

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        self.loaded_files = []
        for file in self.load_default_file():
            file_path = messages_path / file
            self.loaded_files.append(file_path)

        self.name = "set-messages"

    def load_messages_file(self, file_path: Path) -> list[MessageGroup]:
        file_name = file_path.relative_to(messages_path)

        if not file_path.exists() or not file_path.is_file():
            raise ValueError(f"Could not find messages file \"{file_name}\".")

        with file_path.open() as file:
            messages_json = json.load(file)

        if not isinstance(messages_json, List):
            raise ValueError(f"messages file \"{file_name}\" is not formatted correctly.")

        message_groups: List[MessageGroup] = []

        for group in messages_json:
            channel_name = group['channel']
            channel_id = Config.json_config['ch_id'][channel_name]
            channel = self.bot.get_channel(channel_id)

            if not channel:
                raise ValueError(f"Could not find channel \"{group['channel']}\" from messages file \"{file_name}\"")

            if not isinstance(channel, discord.TextChannel):
                raise ValueError(f"channel \"{group['channel']}\" from message file \"{file_name}\" is not a text channel")

            message_groups.append(MessageGroup(str(file_path.relative_to(messages_path)), channel, group['messages'], group["clear_channel"]))

        return message_groups

    @staticmethod
    def load_default_file() -> list[str]:
        if not default_file_name.exists():
            raise ValueError("Could not find default messages file. (should be at shared/messages/default.json)")

        with default_file_name.open() as default_file:
            default_json = json.load(default_file)

        if not isinstance(default_json, List):
            raise ValueError("Default messages file is not formatted correctly.")

        return default_json

    @staticmethod
    async def send_messages(messages: list[MessageGroup] | MessageGroup) -> None:

        if isinstance(messages, MessageGroup):
            messages_list = [messages,]
        else:
            messages_list = messages

        for group in messages_list:
            if group.clear_channel: await group.channel.purge(limit=100)
            for message in group.messages:
                await send_split_message(group.channel, message)

    @app_commands.command(name="from-file")
    @permission_check(Level.LEAD)
    async def send_messages_from_file(self, interaction: discord.Interaction[commands.Bot], location: str) -> None:
        file_location = messages_path / location

        await interaction.response.send_message("Sending message(s)...")

        message_group: list[MessageGroup]
        try:
            message_group = self.load_messages_file(file_location)
        except ValueError as e:
            print(e)
            await interaction.response.send_message(e)
            return

        await self.send_messages(message_group)
        await interaction.followup.send("Message(s) sent!")

    @app_commands.command(name="refresh")
    @permission_check(Level.LEAD)
    async def refresh_messages(self, interaction: discord.Interaction[commands.Bot]) -> None:

        await interaction.response.send_message("Refreshing messages...")

        message_groups: list[MessageGroup] = []

        for file in self.loaded_files:
            try:
                message_groups.extend(self.load_messages_file(file))
            except Exception as e:
                await interaction.followup.send(f"Error loading messages: {e}")

        await self.send_messages(message_groups)

        await interaction.followup.send("Messages refreshed!")

async def setup(bot: commands.Bot) -> None:
    bot.tree.add_command(InfoMessages(bot))