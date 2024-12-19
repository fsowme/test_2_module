import json
import logging
import os
import random
import string
import time

import confluent_kafka as kafka
import dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

CONFIG = {
    'bootstrap.servers': os.environ['BROKER'],
    'acks': os.environ['ACKS'],
    'retries': int(os.environ['RETRIES']),
}
TOPIC_NAME = os.environ['TOPIC_MESSAGES_IN']
QUEUE_FULL_TIMEOUT = os.environ.get('QUEUE_FULL_TIMEOUT', 0)

producer = kafka.Producer(CONFIG)


def fake_message(length: int) -> bytes:
    body = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    message = {'sender': {'username': 'from'}, 'recipient': {'username': 'to'}, 'message': body}
    return json.dumps(message).encode()


while True:
    message = fake_message(random.randint(3, 10))
    logger.info(message)

    try:
        producer.produce(topic=TOPIC_NAME, value=message)
    except BufferError as error:
        logger.error('Internal producer message queue is full, error: %s', error)
        time.sleep(QUEUE_FULL_TIMEOUT)
    except kafka.KafkaException as error:
        logger.error('Something went wrong, message:%s, error: %s', message, error)
        raise

    time.sleep(random.uniform(0.1, 2.0))
