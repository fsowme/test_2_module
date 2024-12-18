import logging

from .handler import app
from .tables import bans as table_bans
from .topics import bans, messages_in, messages_out

logger = logging.getLogger(__name__)


@app.agent(messages_in, sink=[messages_out])
async def messages(stream):
    async for message in stream:
        logger.info('Received message: %s', message)
        yield message


@app.agent(bans)
async def bans(stream):
    async for message in stream:
        logger.info('Received message: %s', message)
        logger.info('1' + str(table_bans[message.blocker.username]))
        banned_users = table_bans[message.blocker.username]
        banned_users.append(message.banned.username)
        table_bans[message.blocker.username] = banned_users
        logger.info('2' + str(table_bans[message.blocker.username]))
        yield message
