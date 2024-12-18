from .config import Config
from .handler import app
from .schemas import message_schema

messages_in = app.topic(Config.topic_messages_in, schema=message_schema)
messages_out = app.topic(Config.topic_messages_out, schema=message_schema)

bans = app.topic(Config.bans_topic)
