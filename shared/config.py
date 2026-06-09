import json
import os
from pathlib import Path

FILE_PATH = Path(os.path.dirname(__file__))

class Config:

    json_config = json.load(open(os.path.join(FILE_PATH, 'bot_config.json')))