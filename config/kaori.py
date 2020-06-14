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


def _get_slack_webhook_tokens(verification_token, webhook_tokens_string):
    tokens = [verification_token]
    if not webhook_tokens_string:
        return tokens

    webhook_tokens = [x.strip(' ') for x in webhook_tokens_string.split(',')]
    return tokens + webhook_tokens


SLACK_WEBHOOK_TOKENS = _get_slack_webhook_tokens(SLACK_VERIFICATION_TOKEN,
                                                 _env('SLACK_WEBHOOK_TOKENS', None))
