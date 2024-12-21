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
    'bootstrap.servers': os.environ['BROKER_EXTERNAL_ADDR'],
    'acks': os.environ['ACKS'],
    'retries': int(os.environ['RETRIES']),
}


def produce(message: bytes, topic_name: str):
    producer = kafka.Producer(CONFIG)
    try:
        producer.produce(topic_name, value=message)
    except kafka.KafkaException as error:
        logger.error('Something went wrong, message:%s, error: %s', message, error)
        raise
    producer.flush()


def test_ban():
    recipient = 'User1'
    banned = 'BadUser'
    good_sender = 'User2'

    ban_message = json.dumps({
        'blocker': {'username': recipient},
        'banned': {'username': banned}
    }).encode('utf-8')

    produce(ban_message, os.environ['TOPIC_BANS'])

    good_message = json.dumps({
        'sender': {'username': good_sender},
        'recipient': {'username': recipient},
        'message': 'Hello world!'
    }).encode('utf-8')

    produce(good_message, os.environ['TOPIC_MESSAGES_IN'])

    banned_message = json.dumps({
        'sender': {'username': banned},
        'recipient': {'username': recipient},
        'message': 'Hello world!'
    }).encode('utf-8')

    produce(banned_message, os.environ['TOPIC_MESSAGES_IN'])


def test_censoring():
    recipient = 'User1'
    sender = 'User2'
    bad_word = 'bad'

    obscene = json.dumps({'word': bad_word}).encode('utf-8')
    produce(obscene, os.environ['TOPIC_OBSCENE_WORDS'])

    bad_message = json.dumps({
        'sender': {'username': sender},
        'recipient': {'username': recipient},
        'message': f'Hello world! {bad_word}. Tssss...'
    }).encode('utf-8')

    produce(bad_message, os.environ['TOPIC_MESSAGES_IN'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Test')
    parser.add_argument('--ban', dest='tests', action='append_const', const=test_ban)
    parser.add_argument('--censorship', dest='tests', action='append_const', const=test_censoring)

    parsed = parser.parse_args()

    for test in parsed.tests:
        test()
