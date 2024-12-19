import argparse
import json
import logging
import os

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
TOPIC_NAME = os.environ['TOPIC_BANS']

producer = kafka.Producer(CONFIG)


def produce(message: bytes):
    try:
        producer.produce(TOPIC_NAME, value=message)
    except kafka.KafkaException as error:
        logger.error('Something went wrong, message:%s, error: %s', message, error)
        raise
    producer.flush()


if __name__ == '__main__':
    parser = argparse.ArgumentParser('producer')

    subparsers = parser.add_subparsers(dest='command', required=True)
    subparsers.metavar = ''

    ban_parser = subparsers.add_parser('ban', help='Ban a user')
    ban_parser.add_argument('--blocker', required=True)
    ban_parser.add_argument('--banned', required=True)

    parsed = parser.parse_args()

    message = {
        'blocker': {'username': parsed.blocker},
        'banned': {'username': parsed.banned}
    }
    raw = json.dumps(message).encode('utf-8')
    produce(raw)
