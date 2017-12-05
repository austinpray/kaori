import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://kizuna:kizuna@db:5432/kizuna')
KIZUNA_ENV = os.environ.get('KIZUNA_ENV', 'development')
KIZUNA_WEB_URL = os.environ.get('KIZUNA_WEB_URL', 'http://localhost:8000')
MAIN_CHANNEL = os.environ.get('MAIN_CHANNEL', '#banter')
SENTRY_URL = os.environ.get('SENTRY_URL', None)
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN', None)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
S3_BUCKET = os.environ.get('S3_BUCKET', 'kizuna.guap.io')
S3_BUCKET_URL = os.environ.get('S3_BUCKET_URL', 'https://s3-us-west-2.amazonaws.com/kizuna.guap.io')
IMAGE_UPLOAD_DIR = os.environ.get('IMAGE_UPLOAD_DIR', 'images')

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise Warning('You have not configured your AWS credentials. Reaction image feature will not work')
