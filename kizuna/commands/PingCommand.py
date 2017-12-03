from kizuna.commands.Command import Command


class PingCommand(Command):
    def __init__(self) -> None:
        help_text = "{bot} ping - respond with pong"

        super().__init__('ping$', "ping", help_text, True)

    def respond(self, slack_client, message, matches):
        self.send(slack_client, message['channel'], 'pong')
