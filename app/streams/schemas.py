import faust

from . import models
from .config import Config

message = faust.Schema(value_type=models.Message, value_serializer=Config.default_serializer)

ban = faust.Schema(value_type=models.Ban, value_serializer=Config.default_serializer)

obscene_word = faust.Schema(value_type=models.ObsceneWord, value_serializer=Config.default_serializer)
