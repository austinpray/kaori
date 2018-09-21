import dramatiq
import spacy
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from raven import Client
from slackclient import SlackClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import \
    RABBITMQ_URL,\
    SENTRY_URL,\
    KIZUNA_ENV,\
    SLACK_API_TOKEN,\
    DATABASE_URL,\
    MAIN_CHANNEL,\
    KIZUNA_HOME_CHANNEL

from src.support.Kizuna import Kizuna
from src.support.commands import \
    AtGraphCommand, ClapCommand, KKredsMiningCommand, \
    KKredsBalanceCommand, LoginCommand, PingCommand, \
    ReactCommand, UserRefreshCommand, KKredsTransactionCommand

rabbitmq_broker = RabbitmqBroker(url=RABBITMQ_URL)
dramatiq.set_broker(rabbitmq_broker)

nlp = spacy.load('en')

DEV_INFO = Kizuna.read_dev_info('./.dev-info.json')

sentry = Client(SENTRY_URL,
                release=DEV_INFO.get('revision'),
                environment=KIZUNA_ENV) if SENTRY_URL else None

if not SLACK_API_TOKEN:
    raise ValueError('You are missing a slack token! Please set the SLACK_API_TOKEN environment variable in your '
                     '.env file or in the system environment')

sc = SlackClient(SLACK_API_TOKEN)
db_engine = create_engine(DATABASE_URL)
make_session = sessionmaker(bind=db_engine)

auth = sc.api_call('auth.test')
bot_id = auth['user_id']

k = Kizuna(bot_id,
           slack_client=sc,
           main_channel=MAIN_CHANNEL,
           home_channel=KIZUNA_HOME_CHANNEL)

# k.handle_startup(DEV_INFO, make_session())

pc = PingCommand()
k.register_command(pc)

lc = LoginCommand(make_session)
k.register_command(lc)

clap = ClapCommand()
k.register_command(clap)

at_graph_command = AtGraphCommand(make_session)
k.register_command(at_graph_command)

user_refresh_command = UserRefreshCommand(db_session=make_session)
k.register_command(user_refresh_command)

react_command = ReactCommand(make_session, nlp=nlp)
k.register_command(react_command)

kkreds_command = KKredsMiningCommand(make_session, kizuna=k)
k.register_command(kkreds_command)

kkreds_balance_command = KKredsBalanceCommand(make_session)
k.register_command(kkreds_balance_command)

kkreds_transaction_command = KKredsTransactionCommand(make_session, kizuna=k)
k.register_command(kkreds_transaction_command)


@dramatiq.actor
def worker(payload):
    if payload['type'] == 'message':
        k.handle_message(payload)
