import logging

from . import handler, tables, topics

logger = logging.getLogger(__name__)


@handler.app.agent(topics.messages_in)
async def messages(stream):
    async for message in stream:
        if message.sender.username in tables.bans[message.recipient.username]:
            logger.info('Sender %s banned by %s', message.sender.username, message.recipient.username)
            await topics.messages_out.send(value=message)


@handler.app.agent(topics.bans)
async def bans(stream):
    async for message in stream:
        banned_users = tables.bans[message.blocker.username]
        if message.banned.username not in banned_users:
            banned_users.append(message.banned.username)
            tables.bans[message.blocker.username] = banned_users
            logger.info('User "%s" banned by "%s"', message.banned.username, message.blocker.username)
