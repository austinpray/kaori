from slacktools.chat import reply

from .BaseCommand import BaseCommand
from ..models import User


class KKredsBalanceCommand(BaseCommand):
    def __init__(self, make_session) -> None:
        help_text = 'kizuna balance - show your kkreds balance'

        super().__init__(name='kkred-balance',
                         pattern='balance$',
                         help_text=help_text,
                         is_at=True,
                         db_session_maker=make_session)

    def respond(self, slack_client, message, matches):
        user_id = message['user']

        with self.db_session_scope() as session:
            user = User.get_by_slack_id(session, user_id)
            balance = user.get_kkred_balance(session)

        pluralized_kkreds = 'kkred' if balance == 1 else 'kkreds'
        return reply(slack_client, message, f'your balance is {balance} {pluralized_kkreds}')
