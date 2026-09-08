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

FILE_PATH = Path(os.path.dirname(__file__))

# Swap when using the test server
BOT_CONFIG = 'bot_config.json'
# BOT_CONFIG = 'test_server_config.json'

class Config:

    json_config = json.load(open(os.path.join(FILE_PATH, BOT_CONFIG)))