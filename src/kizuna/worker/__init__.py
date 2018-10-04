import logging

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from raven import Client
from slackclient import SlackClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import kizuna.plugins.chat
import kizuna.plugins.clap
import kizuna.plugins.ping
from kizuna.adapters.slack import SlackAdapter
from kizuna.skills import DB
from kizuna.support import Kizuna
from kizuna.support.dev_info import read_dev_info

logging.basicConfig(level=logging.DEBUG)

DEV_INFO = read_dev_info('./.dev-info.json')

sentry = Client(config.SENTRY_URL,
                release=DEV_INFO.get('revision'),
                environment=config.KIZUNA_ENV) if config.SENTRY_URL else None

rabbitmq_broker = RabbitmqBroker(url=config.RABBITMQ_URL)
dramatiq.set_broker(rabbitmq_broker)

if not config.SLACK_API_TOKEN:
    raise ValueError('You are missing a slack token! Please set the SLACK_API_TOKEN environment variable in your '
                     '.env file or in the system environment')

sc = SlackClient(config.SLACK_API_TOKEN)
db_engine = create_engine(config.DATABASE_URL)
make_session = sessionmaker(bind=db_engine)

k = Kizuna()

k.adapters['slack'] = SlackAdapter(slack_client=sc)

k.skills |= {
    DB(make_session=make_session),
}

k.plugins |= {
    kizuna.plugins.chat,
    kizuna.plugins.clap,
    kizuna.plugins.ping,
}


@dramatiq.actor
def slack_worker(payload):
    logging.debug(payload)
    k.handle('slack', payload)
