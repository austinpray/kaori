import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

db_engine = create_engine(config.DATABASE_URL)
make_db_session = sessionmaker(bind=db_engine)

if not config.AWS_ACCESS_KEY_ID or not config.AWS_SECRET_ACCESS_KEY:
    raise Warning('You have not configured your AWS credentials. Reaction image feature will not work')

aws_client = boto3.client(
    's3',
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)
