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

from typing import List, Any

import discord
import os
from pathlib import Path
from dotenv import load_dotenv

from shared.transpeak_bot import TranspeakBot


class TransBot(TranspeakBot):
    def __init__(self, bot_extensions: list[str], intents: discord.Intents, **kwargs: Any):
        super().__init__(bot_extensions, intents, **kwargs)

class Main:

    TBOT_DIR = Path(__file__).resolve().parent

    bot_extensions: List[str] = [
        'extensions.manage_extensions'
    ]

    intents = discord.Intents.all()

    def run(self) -> None:
        load_dotenv(dotenv_path=self.TBOT_DIR / '..' / '.env')

        token = os.getenv("TBOT_TOKEN")
        if not token:
            raise ValueError("TransBot token not found in .env file.")

        discord.utils.setup_logging()

        client = TransBot(self.bot_extensions, self.intents, command_prefix='!', help_command=None)
        client.run(token)

if __name__ == "__main__":
    Main().run()