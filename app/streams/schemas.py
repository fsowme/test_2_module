import faust

from .config import Config
from .models import User

message_schema = faust.Schema(value_type=User, value_serializer=Config.default_serializer)
