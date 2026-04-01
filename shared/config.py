import json
import os

JSON_PATH = os.path.join(os.path.dirname(__file__), 'bot_config.json')

class Config:

    json_config = json.load(open(JSON_PATH))