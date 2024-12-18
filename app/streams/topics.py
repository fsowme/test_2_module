from .config import Config
from .handler import app

messages_in = app.topic(Config.topic_messages_in)
messages_out = app.topic(Config.topic_messages_out)

bans = app.topic(Config.bans_topic)
