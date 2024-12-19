import faust

from .config import Config

app = faust.App(
    id=Config.default_app_name,
    broker=Config.broker,
    store=Config.store,
    topic_replication_factor=3,
    topic_partitions=3
)
