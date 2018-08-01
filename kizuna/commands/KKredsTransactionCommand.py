from kizuna.Kizuna import Kizuna
from kizuna.commands.Command import Command
from kizuna.models.KKredsTransaction import KKredsTransaction
from kizuna.models.User import User
import arrow
from kizuna.slack import is_user_mention, get_user_id_from_mention
from decimal import Decimal, InvalidOperation


class KKredsTransactionCommand(Command):
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
                return self.reply(slack_client,
                                  message,
                                  'User has to be an `@` mention. Like it has to be a real blue `@` mention.')

            receiving_user = User.get_by_slack_id(session,
                                                  get_user_id_from_mention(receiving_user_raw))

            if not receiving_user:
                return self.reply(slack_client, message, 'Could not find that user')

            if sending_user.id == receiving_user.id:
                return self.reply(slack_client,
                                  message,
                                  'You can’t send money to yourself.')

            amount_raw = matches[1]

            try:
                amount = Decimal(amount_raw)
            except InvalidOperation:
                return self.reply(slack_client,
                                  message,
                                  'That amount is invalid. Try a decimal or integer value')

            if amount <= 0:
                return self.reply(slack_client,
                                  message,
                                  'Amount has to be non-zero')

            if amount > sending_user.get_kkred_balance(session):
                return self.reply(slack_client,
                                  message,
                                  'You don’t have enough kkreds')

            transaction = KKredsTransaction(from_user=sending_user,
                                            to_user=receiving_user,
                                            amount=amount,
                                            created_at=message_ts.datetime)

            session.add(transaction)

            self.reply(slack_client, message, f'successfully sent {amount} to {receiving_user.name}')
