import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://kizuna:kizuna@db:5432/kizuna')
KIZUNA_ENV = os.environ.get('KIZUNA_ENV', 'development')
MAIN_CHANNEL = os.environ.get('MAIN_CHANNEL', '#banter')
SENTRY_URL = os.environ.get('SENTRY_URL', None)
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN', None)
