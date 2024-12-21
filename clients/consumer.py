import logging
import dotenv
from confluent_kafka import Consumer

import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()


CONFIG = {
    'bootstrap.servers': os.environ['BROKER_EXTERNAL_ADDR'],
    'group.id': os.environ['GROUP_ID'],
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True,
}
TOPIC_NAME = os.environ['TOPIC_MESSAGES_OUT']

consumer = Consumer(CONFIG)
consumer.subscribe([TOPIC_NAME])


try:
    while True:
        msg = consumer.poll(0.5)

        if msg is None:
            continue

        error = msg.error()
        if error is not None:
            logger.error(f"Ошибка: {error}")
            continue

        raw = msg.value()

        message = json.loads(raw)

        logger.info(f"Получено сообщение: {message}, offset={msg.offset()}, partition={msg.partition()}")

finally:
    consumer.close()
