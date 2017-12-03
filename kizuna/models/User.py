from sqlalchemy import Column, Integer, String
from kizuna.models.Models import Base
from secrets import token_hex


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
