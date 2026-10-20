import dataclasses
import json
import os
from pathlib import Path
from typing import List

import discord
from discord import app_commands
from discord.ext import commands

from shared.utils.permissions import permission_check, Level

project_path = Path(os.path.dirname(__file__)).parent
messages_path = project_path / "shared" / "messages"
default_file_name = messages_path / "default.json"


@dataclasses.dataclass
class MessageGroup:
    file_name: str
    channel: discord.TextChannel
    messages: List[str]

class InfoMessages(app_commands.Group):

    loaded_files: List[Path]

    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

        for file in self.load_default_file():
            file_path = messages_path / file
            self.loaded_files.append(file_path)

    def load_messages_file(self, file_path: Path) -> list[MessageGroup]:
        file_name = file_path.relative_to(messages_path)

        if not file_path.exists():
            raise ValueError(f"Could not find messages file \"{file_name}\".")

        with file_path.open() as file:
            messages_json = json.load(file)

        if not isinstance(messages_json, List):
            raise ValueError(f"messages file \"{file_name}\" is not formatted correctly.")

        message_groups: List[MessageGroup] = []

        for group in messages_json:
            channel = self.bot.get_channel(group['channel'])

            if not channel:
                raise ValueError(f"Could not find channel \"{group['channel']}\" from messages file \"{file_name}\"")

            if not isinstance(channel, discord.TextChannel):
                raise ValueError(f"channel \"{group['channel']}\" from message file \"{file_name}\" is not a text channel")

            message_groups.append(MessageGroup(str(file_path.relative_to(messages_path)), channel, group['messages']))

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


    @app_commands.command()
    @permission_check(Level.LEAD)
    async def refresh_messages(self, interaction: discord.Interaction[commands.Bot]) -> None:

        await interaction.response.send_message("")