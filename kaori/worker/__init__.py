import importlib.util
import logging
import os

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from raven import Client
from slackclient import SlackClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import kaori.plugins.chat
import kaori.plugins.clap
import kaori.plugins.gacha
import kaori.plugins.kkreds
import kaori.plugins.ping
import kaori.plugins.users
from kaori.adapters.slack import SlackAdapter
from kaori.skills import DB
from kaori.support import Kaori

logging.basicConfig(level=logging.DEBUG)

# DEV_INFO = read_dev_info('./.dev-info.json')

spec = importlib.util.spec_from_file_location("config.kaori", os.path.join(os.getcwd(), 'config/kaori.py'))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

sentry = Client(config.SENTRY_URL,
                # release=DEV_INFO.get('revision'),
                environment=config.KIZUNA_ENV) if config.SENTRY_URL else None

rabbitmq_broker = RabbitmqBroker(url=config.RABBITMQ_URL)
dramatiq.set_broker(rabbitmq_broker)

if not config.SLACK_API_TOKEN:
    raise ValueError('You are missing a slack token! Please set the SLACK_API_TOKEN environment variable in your '
                     '.env file or in the system environment')

sc = SlackClient(config.SLACK_API_TOKEN)
db_engine = create_engine(config.DATABASE_URL)
make_session = sessionmaker(bind=db_engine, autoflush=False)

k = Kaori()

k.adapters['slack'] = SlackAdapter(slack_client=sc)

k.skills |= {
    DB(make_session=make_session),
}

k.plugins |= {
    kaori.plugins.chat,
    kaori.plugins.clap,
    kaori.plugins.ping,
    kaori.plugins.users,
    kaori.plugins.kkreds,
    kaori.plugins.gacha,
}


@dramatiq.actor
def slack_worker(payload):
    logging.debug(payload)
    k.handle('slack', payload)
