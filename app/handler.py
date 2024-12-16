import logging
import os

import dotenv
import faust

logger = logging.getLogger(__name__)
dotenv.load_dotenv()

app = faust.App(
    'test-2', broker=os.environ['BROKER'], value_serializer="raw", store=os.environ['STORE']
)

messages_topic = app.topic(os.environ['MESSAGES_TOPIC'])
bans_topic = app.topic(os.environ['BANS_TOPIC'])


@app.agent(messages_topic)
async def messages(stream):
    async for message in stream:
        logger.debug('Received message: %s', message)


@app.agent(bans_topic)
async def bans(stream):
    async for ban in stream:
        logger.debug('Received ban: %s', ban)
