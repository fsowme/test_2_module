import faust

from .config import Config
from .models import Ban, Message

message_schema = faust.Schema(value_type=Message, value_serializer=Config.default_serializer)

ban_schema = faust.Schema(value_type=Ban, value_serializer=Config.default_serializer)
