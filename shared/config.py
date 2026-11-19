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

import json
import os
from pathlib import Path

from dotenv import load_dotenv
FILE_PATH = Path(os.path.dirname(__file__))
env_file_path = FILE_PATH / ".." / ".env"
load_dotenv(env_file_path)

BOT_CONFIG = os.getenv("BOT_CONFIG")
if BOT_CONFIG is None:
    raise ValueError("bot config not found in .env file")
bot_config_str: str = BOT_CONFIG # to make type checkers happy

class Config:

    json_config = json.load(open(os.path.join(FILE_PATH, bot_config_str)))