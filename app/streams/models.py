import logging

import faust

logger = logging.getLogger(__name__)


class User(faust.Record):
    username: str


class Message(faust.Record):
    sender: User
    recipient: User
    message: str


class Ban(faust.Record):
    blocker: User
    banned: User


class ObsceneWord(faust.Record):
    word: str
