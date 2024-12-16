import argparse
import os

import confluent_kafka
import dotenv

dotenv.load_dotenv()

CONFIG = {
    'bootstrap.servers': os.environ['BROKER'],
    'acks': os.environ['ACKS'],
    'retries': os.environ['RETRIES']
}

producer = confluent_kafka.Producer(CONFIG)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Producer', description='Produce messages to Kafka topics.')
    subparser = parser.add_subparsers(title='COMMANDS')
    subparser.metavar = ''

    send_message = subparser.add_parser('send', help='Send message')
    send_message.add_argument('--from', required=True)
    send_message.add_argument('--to', required=True)
    send_message.add_argument('message', help='Text message')

    ban = subparser.add_parser('ban', help='Ban user')
    ban.add_argument('--blocker', required=True)
    ban.add_argument('--banned', required=True)

    args = parser.parse_args()
