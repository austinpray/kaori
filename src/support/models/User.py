from decimal import Decimal
from secrets import token_hex

from cryptography.fernet import Fernet
from sqlalchemy import Column, Integer, String, func

from config import FERNET_KEY, FERNET_TTL
from src.support.models.KKredsTransaction import KKredsTransaction
from src.support.models.Models import Base


def user_generate_api_key():
    token = token_hex(32)
    return 'kiz-{}'.format(token)


class User(Base):
    @staticmethod
    def generate_api_key():
        user_generate_api_key()

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slack_id = Column(String, index=True, unique=True)
    api_key = Column(String(), unique=True, index=True, nullable=False, default=user_generate_api_key)

    def __repr__(self):
        return "<User(id='{}', name='{}', slack_id='{}')>".format(self.id, self.name, self.slack_id)

    @staticmethod
    def get_by_slack_id(session, slack_id) -> 'User':
        return session.query(User).filter(User.slack_id == slack_id).first()

    @staticmethod
    def decrypt_token(token):
        if isinstance(token, str):
            token = token.encode('ascii')

        f = Fernet(FERNET_KEY)
        return f.decrypt(token, ttl=FERNET_TTL).decode('ascii')

    def get_token(self):
        f = Fernet(FERNET_KEY)
        return f.encrypt(self.api_key.encode('ascii'))

    def get_kkred_balance(self, session) -> Decimal:
        kkred_debits = session \
            .query(func.sum(KKredsTransaction.amount)) \
            .filter(KKredsTransaction.from_user_id == self.id) \
            .first()[0]

        if kkred_debits is None:
            kkred_debits = Decimal(0)

        kkred_credits = session \
            .query(func.sum(KKredsTransaction.amount)) \
            .filter(KKredsTransaction.to_user_id == self.id) \
            .first()[0]

        if kkred_credits is None:
            kkred_credits = Decimal(0)

        return kkred_credits - kkred_debits

    @staticmethod
    def maybe_create_user_from_slack_id(slack_id, slack_client, session):
        from_user = session.query(User).filter(User.slack_id == slack_id).first()
        if from_user:
            return from_user

        slack_user_res = slack_client.api_call("users.info", user=slack_id)
        if not slack_user_res['ok']:
            raise ValueError("couldn't get user {} from slack api".format(slack_id))

        slack_user = slack_user_res['user']
        from_user = User(name=slack_user['name'], slack_id=slack_user['id'])
        session.add(from_user)
        return from_user
