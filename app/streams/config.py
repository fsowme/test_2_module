import os
from dataclasses import dataclass

import dotenv

dotenv.load_dotenv()


@dataclass
class _Config:
    broker: str = os.environ['BROKER']
    store: str = os.environ['STORE']
    messages_topics: str = os.environ['MESSAGES_TOPIC']
    bans_topic: str = os.environ['BANS_TOPIC']
    default_serializer: str = 'json'
    default_app_name: str = 'test-2'


Config = _Config()
