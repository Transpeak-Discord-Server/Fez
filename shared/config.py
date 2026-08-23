import json
import os
from pathlib import Path

FILE_PATH = Path(os.path.dirname(__file__))

# Swap when using the test server
BOT_CONFIG = 'bot_config.json'
# BOT_CONFIG = 'test_server_config.json'

class Config:

    json_config = json.load(open(os.path.join(FILE_PATH, BOT_CONFIG)))