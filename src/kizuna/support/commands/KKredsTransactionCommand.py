from decimal import Decimal, InvalidOperation

import arrow
from slacktools.chat import reply
from slacktools.message import is_user_mention, extract_user_id_from_mention

from .slack_command import SlackCommand
from .. import Kizuna
from ..models import KKredsTransaction, User


class KKredsTransactionCommand(SlackCommand):
    def __init__(self, make_session, kizuna: Kizuna) -> None:
        self.kizuna = kizuna

        help_text = 'kizuna pay <user> <amount> - pay the user that amount of kkreds'

        pattern = "(?:pay|tip|give|send) (\S*) (\S*)"

        super().__init__('send_kkred', pattern, help_text, is_at=True, db_session_maker=make_session)

    def respond(self, slack_client, message, matches):
        message_ts = arrow.get(message['event_ts'])

        sending_user_id = message['user']

        with self.db_session_scope() as session:
            sending_user = User.get_by_slack_id(session, sending_user_id)

            if not sending_user:
                return

            receiving_user_raw = matches[0]

            if not is_user_mention(receiving_user_raw):
                return reply(slack_client,
                             message,
                             'User has to be an `@` mention. Like it has to be a real blue `@` mention.')

            receiving_user = User.get_by_slack_id(session,
                                                  extract_user_id_from_mention(receiving_user_raw))

            if not receiving_user:
                return reply(slack_client, message, 'Could not find that user')

            if sending_user.id == receiving_user.id:
                return reply(slack_client,
                             message,
                             'You can’t send money to yourself.')

            amount_raw = matches[1]

            try:
                amount = Decimal(amount_raw)
            except InvalidOperation:
                return reply(slack_client,
                             message,
                             'That amount is invalid. Try a decimal or integer value')

            if amount <= 0:
                return reply(slack_client,
                             message,
                             'Amount has to be non-zero')

            if amount > sending_user.get_kkred_balance(session):
                return reply(slack_client,
                             message,
                             'You don’t have enough kkreds')

            transaction = KKredsTransaction(from_user=sending_user,
                                            to_user=receiving_user,
                                            amount=amount,
                                            created_at=message_ts.datetime)

            session.add(transaction)

            reply(slack_client, message, f'successfully sent {amount} to {receiving_user.name}')
