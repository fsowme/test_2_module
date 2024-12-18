import faust

from .config import Config
from .models import Message

message_schema = faust.Schema(value_type=Message, value_serializer=Config.default_serializer)
