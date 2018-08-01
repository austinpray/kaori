from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from slackclient import SlackClient

from kizuna.Kizuna import Kizuna
from kizuna.commands.AtGraphCommand import AtGraphCommand
from kizuna.commands.AtGraphDataCollector import AtGraphDataCollector
from kizuna.commands.ClapCommand import ClapCommand
from kizuna.commands.KKredsMiningCommand import KKredsMiningCommand
from kizuna.commands.KKredsBalanceCommand import KKredsBalanceCommand
from kizuna.commands.LoginCommand import LoginCommand
from kizuna.commands.PingCommand import PingCommand
from kizuna.commands.ReactCommand import ReactCommand
from kizuna.commands.UserRefreshCommand import UserRefreshCommand
from kizuna.commands.KKredsTransactionCommand import KKredsTransactionCommand

import spacy

from raven import Client
import config
import dramatiq

from dramatiq.brokers.rabbitmq import RabbitmqBroker

rabbitmq_broker = RabbitmqBroker(url=config.RABBITMQ_URL)
dramatiq.set_broker(rabbitmq_broker)

nlp = spacy.load('en')

DEV_INFO = Kizuna.read_dev_info('./.dev-info.json')

sentry = Client(config.SENTRY_URL,
                release=DEV_INFO.get('revision'),
                environment=config.KIZUNA_ENV) if config.SENTRY_URL else None

if not config.SLACK_API_TOKEN:
    raise ValueError('You are missing a slack token! Please set the SLACK_API_TOKEN environment variable in your '
                     '.env file or in the system environment')

sc = SlackClient(config.SLACK_API_TOKEN)
db_engine = create_engine(config.DATABASE_URL)
make_session = sessionmaker(bind=db_engine)

auth = sc.api_call('auth.test')
bot_id = auth['user_id']

k = Kizuna(bot_id,
           slack_client=sc,
           main_channel=config.MAIN_CHANNEL,
           home_channel=config.KIZUNA_HOME_CHANNEL)

# k.handle_startup(DEV_INFO, make_session())

pc = PingCommand()
k.register_command(pc)

lc = LoginCommand(make_session)
k.register_command(lc)

clap = ClapCommand()
k.register_command(clap)

at_graph_command = AtGraphCommand(make_session)
k.register_command(at_graph_command)

at_graph_data_collector = AtGraphDataCollector(make_session, sc)
k.register_command(at_graph_data_collector)

user_refresh_command = UserRefreshCommand(db_session=make_session)
k.register_command(user_refresh_command)

react_command = ReactCommand(make_session, nlp=nlp)
k.register_command(react_command)

kkreds_command = KKredsMiningCommand(make_session, kizuna=k)
k.register_command(kkreds_command)

kkreds_balance_command = KKredsBalanceCommand(make_session, kizuna=k)
k.register_command(kkreds_balance_command)

kkreds_transaction_command = KKredsTransactionCommand(make_session, kizuna=k)
k.register_command(kkreds_transaction_command)


@dramatiq.actor
def worker(payload):
    if payload['type'] == 'message':
        k.handle_message(payload)
