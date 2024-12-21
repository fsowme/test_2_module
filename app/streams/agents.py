import logging
import re

from . import handler, tables, topics

logger = logging.getLogger(__name__)

CENSORSHIP_MASK = '<CENSORED>'


@handler.app.agent(topics.messages_in, sink=[topics.censor])
async def messages(stream):
    async for message in stream:
        if message.sender.username in tables.bans[message.recipient.username]:
            logger.info('Sender %s banned by %s', message.sender.username, message.recipient.username)
            continue


@handler.app.agent(topics.censor, sink=[topics.messages_out])
async def censor(stream):
    async for message in stream:
        pattern = r'\b(' + '|'.join(tables.obscene_words.keys()) + r')\b'
        message.message = re.sub(pattern, CENSORSHIP_MASK, message.message)
        yield message


@handler.app.agent(topics.bans)
async def bans(stream):
    async for message in stream:
        banned_users = tables.bans[message.blocker.username]
        if message.banned.username not in banned_users:
            banned_users.append(message.banned.username)
            tables.bans[message.blocker.username] = banned_users
            logger.info('User "%s" banned by "%s"', message.banned.username, message.blocker.username)


@handler.app.agent(topics.obscene_words)
async def obscene_words(stream):
    async for message in stream:
        if message.word not in tables.obscene_words:
            tables.obscene_words[message.word] = True
            logger.info('Obscene word added to dictionary')
