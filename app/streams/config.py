import os
from dataclasses import dataclass

import dotenv

dotenv.load_dotenv()


@dataclass
class _Config:
    broker: str = os.environ['BROKER']
    store: str = os.environ['STORE']
    topic_messages_in: str = os.environ['TOPIC_MESSAGES_IN']
    topic_messages_out: str = os.environ['TOPIC_MESSAGES_OUT']
    topic_bans: str = os.environ['TOPIC_BANS']
    topic_obscene_words: str = os.environ['TOPIC_OBSCENE_WORDS']
    default_serializer: str = 'json'
    default_app_name: str = 'test-2'


Config = _Config()
