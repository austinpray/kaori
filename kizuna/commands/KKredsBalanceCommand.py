from kizuna.commands.Command import Command
from kizuna.models.User import User
from kizuna.Kizuna import Kizuna


class KKredsBalanceCommand(Command):
    def __init__(self, make_session, kizuna: Kizuna) -> None:
        self.make_session = make_session

        help_text = 'kizuna balance - show your kkreds balance'

        kizuna_resp_token_regex = '|'.join(kizuna.respond_tokens)
        triggers = [
            "(?:(?:m|M)olly|<@U04EQPCC8>) ?balance$",
            f"(?:{kizuna_resp_token_regex}) ?balance$"
        ]

        pattern = "|".join(triggers)
        super().__init__('ping$', pattern, help_text, is_at=False, always=True)

    def respond(self, slack_client, message, matches):
        session = self.make_session()

        user_id = message['user']

        user = User.get_by_slack_id(session, user_id)

        balance = user.get_kkred_balance(session)

        pluralized_kkreds = 'kkred' if balance == 1 else 'kkreds'
        return self.reply(slack_client, message, f'your balance is {balance} {pluralized_kkreds}')
