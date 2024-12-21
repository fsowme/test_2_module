from . import schemas
from .config import Config
from .handler import app

messages_in = app.topic(Config.topic_messages_in, schema=schemas.message)
censor = app.topic(Config.topic_censor, schema=schemas.message)
messages_out = app.topic(Config.topic_messages_out, schema=schemas.message)

bans = app.topic(Config.topic_bans, schema=schemas.ban)
obscene_words = app.topic(Config.topic_obscene_words, schema=schemas.obscene_word)
