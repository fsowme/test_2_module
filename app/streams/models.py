import logging

import faust

logger = logging.getLogger(__name__)


class User(faust.Record):
    username: str


class Message(faust.Record):
    sender: User
    receiver: User
    message: str
