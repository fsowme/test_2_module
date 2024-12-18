from .config import Config
from .handler import app

messages_topic = app.topic(Config.messages_topics)
bans_topic = app.topic(Config.bans_topic)
