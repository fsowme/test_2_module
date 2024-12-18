import logging

from .handler import app
from .topics import bans_topic, messages_topic

logger = logging.getLogger(__name__)


@app.agent(messages_topic)
async def messages(stream):
    async for message in stream:
        logger.debug('Received message: %s', message)


@app.agent(bans_topic)
async def bans(stream):
    async for ban in stream:
        logger.debug('Received ban: %s', ban)
