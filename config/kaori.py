import base64
import json
import os


def _env(*args, **kwargs):
    return os.environ.get(*args, **kwargs)


API_KEY = _env('KIZUNA_API_KEY', None)
DATABASE_URL = _env('DATABASE_URL', 'postgresql://kaori:kaori@db:5432/kaori')
KIZUNA_ENV = _env('KIZUNA_ENV', 'development')
KIZUNA_HOME_CHANNEL = _env('KIZUNA_HOME_CHANNEL', '#kaori-home')
MAIN_CHANNEL = _env('MAIN_CHANNEL', '#banter')
SENTRY_URL = _env('SENTRY_URL', None)
SLACK_API_TOKEN = _env('SLACK_API_TOKEN', None)
SLACK_VERIFICATION_TOKEN = _env('SLACK_VERIFICATION_TOKEN', None)
SLACK_SIGNING_SECRET = _env('SLACK_SIGNING_SECRET', None)

RABBITMQ_URL = _env('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/%2F')

# To authorize GCP you need to have a service account key.
# https://console.cloud.google.com/iam-admin/serviceaccounts
# The environment variable is a Base64 encoded JSON service account key.
# To encode a JSON file use: base64 -w0 ~/<account_id>.json
GCLOUD_SERVICE_ACCOUNT_INFO = _env('GCLOUD_SERVICE_ACCOUNT_INFO', None)

if GCLOUD_SERVICE_ACCOUNT_INFO:
    GCLOUD_SERVICE_ACCOUNT_INFO = json.loads(base64.b64decode(GCLOUD_SERVICE_ACCOUNT_INFO, validate=True))

IMAGES_BUCKET_GCLOUD = _env('IMAGES_BUCKET_GCLOUD', None)
IMAGES_BUCKET_PATH = '/usr/img'

USE_GCLOUD_STORAGE = bool(
    GCLOUD_SERVICE_ACCOUNT_INFO and
    IMAGES_BUCKET_GCLOUD
)


def _get_slack_webhook_tokens(verification_token, webhook_tokens_string):
    tokens = [verification_token]
    if not webhook_tokens_string:
        return tokens

    webhook_tokens = [x.strip(' ') for x in webhook_tokens_string.split(',')]
    return tokens + webhook_tokens


SLACK_WEBHOOK_TOKENS = _get_slack_webhook_tokens(SLACK_VERIFICATION_TOKEN,
                                                 _env('SLACK_WEBHOOK_TOKENS', None))

GACHA_BATTLE_URL_BASE = _env('GACHA_BATTLE_URL_BASE', None)
