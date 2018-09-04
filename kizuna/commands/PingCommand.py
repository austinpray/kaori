from kizuna.commands import BaseCommand
from kizuna.slack import send


class PingCommand(BaseCommand):
    def __init__(self) -> None:
        help_text = "{bot} ping - respond with pong"

        super().__init__(name='ping$',
                         pattern="ping$",
                         help_text=help_text,
                         is_at=True)

    def respond(self, slack_client, message, matches):
        send(slack_client, message['channel'], 'pong')
