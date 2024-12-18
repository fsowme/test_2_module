import logging

from .handler import app
from .topics import messages_in, messages_out

logger = logging.getLogger(__name__)


@app.agent(messages_in, sink=[messages_out])
async def messages(stream):
    async for message in stream:
        logger.info('Received message: %s', message)
        yield message
