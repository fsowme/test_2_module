import faust

from .config import Config

app = faust.App(Config.default_app_name, broker=Config.broker, store=Config.store)
