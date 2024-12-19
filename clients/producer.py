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

producer = kafka.Producer(CONFIG)


def produce(message: bytes, topic_name: str):
    try:
        producer.produce(topic_name, value=message)
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

    message_parser = subparsers.add_parser('message', help='Send message')
    message_parser.add_argument('--sender', required=True)
    message_parser.add_argument('--recipient', required=True)
    message_parser.add_argument('message')

    obscene_words_parser = subparsers.add_parser('obscene_words', help='Add obscene words')
    obscene_words_parser.add_argument('word')

    parsed = parser.parse_args()

    if parsed.command == 'ban':
        message = {
            'blocker': {'username': parsed.blocker},
            'banned': {'username': parsed.banned}
        }
        topic_name = os.environ['TOPIC_BANS']
    elif parsed.command == 'message':
        message = {
            'sender': {'username': parsed.sender},
            'recipient': {'username': parsed.recipient},
            'message': parsed.message
        }
        topic_name = os.environ['TOPIC_MESSAGES_IN']
    else:
        message = {'word': parsed.word}
        topic_name = os.environ['TOPIC_OBSCENE_WORDS']

    raw = json.dumps(message).encode('utf-8')
    produce(raw, topic_name)
