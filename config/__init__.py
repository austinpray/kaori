import os
from .constants import DAY_IN_SECONDS

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://kizuna:kizuna@db:5432/kizuna')
IMAGE_UPLOAD_DIR = os.environ.get('IMAGE_UPLOAD_DIR', 'images')
KIZUNA_ENV = os.environ.get('KIZUNA_ENV', 'development')
KIZUNA_HOME_CHANNEL = os.environ.get('KIZUNA_HOME_CHANNEL', '#kizuna-home')
KIZUNA_WEB_URL = os.environ.get('KIZUNA_WEB_URL', 'http://localhost:8000')
MAIN_CHANNEL = os.environ.get('MAIN_CHANNEL', '#banter')
S3_BUCKET = os.environ.get('S3_BUCKET', 'kizuna.guap.io')
S3_BUCKET_URL = os.environ.get('S3_BUCKET_URL', 'https://s3-us-west-2.amazonaws.com/kizuna.guap.io')
SECRET_KEY = os.environ.get('SECRET_KEY', None)
SENTRY_URL = os.environ.get('SENTRY_URL', None)
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN', None)

FERNET_KEY = os.environ.get('FERNET_KEY', None)
if FERNET_KEY:
    FERNET_KEY = FERNET_KEY.encode('ascii')

FERNET_TTL = DAY_IN_SECONDS if KIZUNA_ENV != 'development' else 30*DAY_IN_SECONDS
