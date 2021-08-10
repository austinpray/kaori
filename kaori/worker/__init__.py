import logging
import os

# test :^)

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from google.cloud import storage
from google.oauth2 import service_account
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
from kaori.skills import DB, LocalFileUploader, GCloudStorageUploader
from kaori.support import Kaori
from kaori.support.config import get_config
from kaori.plugins.gacha.skills import CardBattler

logging.basicConfig(level=logging.INFO)

config = get_config(os.path.join(os.getcwd(), 'config/kaori.py'))

if hasattr(config, 'SENTRY_URL') and config.SENTRY_URL:  # pragma: no cover
    import sentry_sdk

    sentry_sdk.init(dsn=config.SENTRY_URL,
                    environment=config.KIZUNA_ENV,
                    traces_sample_rate=1)

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

if hasattr(config, 'USE_GCLOUD_STORAGE') and config.USE_GCLOUD_STORAGE:
    creds = service_account.Credentials.from_service_account_info(config.GCLOUD_SERVICE_ACCOUNT_INFO)
    bucket = storage.Client(project=creds.project_id, credentials=creds).bucket(config.IMAGES_BUCKET_GCLOUD)

    k.skills.add(GCloudStorageUploader(bucket=bucket,
                                       base_path=config.IMAGES_BUCKET_PATH))

elif config.KIZUNA_ENV == 'development':
    k.skills.add(LocalFileUploader())
else:
    k.logger.warning('no file upload handler specified!')

if hasattr(config, 'GACHA_BATTLE_URL_BASE') and config.GACHA_BATTLE_URL_BASE:
    k.skills.add(CardBattler(player_url_base=config.GACHA_BATTLE_URL_BASE))
elif config.KIZUNA_ENV == 'development':
    k.skills.add(CardBattler(player_url_base='http://localhost:8080/battle/'))
else:
    k.logger.warning('No gacha battle url set!')

k.plugins |= {
    # kaori.plugins.chat,
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
