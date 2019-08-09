import os

API_KEY = os.environ.get('KIZUNA_API_KEY', None)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://kaori:kaori@db:5432/kaori')
KIZUNA_ENV = os.environ.get('KIZUNA_ENV', 'development')
KIZUNA_HOME_CHANNEL = os.environ.get('KIZUNA_HOME_CHANNEL', '#kaori-home')
MAIN_CHANNEL = os.environ.get('MAIN_CHANNEL', '#banter')
SENTRY_URL = os.environ.get('SENTRY_URL', None)
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN', None)
SLACK_VERIFICATION_TOKEN = os.environ.get('SLACK_VERIFICATION_TOKEN', None)
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET', None)

RABBITMQ_URL = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/%2F')


def get_slack_webhook_tokens(verification_token, webhook_tokens_string):
    tokens = [verification_token]
    if not webhook_tokens_string:
        return tokens

    webhook_tokens = [x.strip(' ') for x in webhook_tokens_string.split(',')]
    return tokens + webhook_tokens


SLACK_WEBHOOK_TOKENS = get_slack_webhook_tokens(SLACK_VERIFICATION_TOKEN,
                                                os.environ.get('SLACK_WEBHOOK_TOKENS', None))
