import re

from slacktools.chat import send

from .slack_command import SlackCommand


class HelpCommand(SlackCommand):
    """usage: {bot} help - display this message"""

    def __init__(self) -> None:
        help_text = "{bot} help - display this message"

        tokens = '|'.join(['-h', '--help', 'help', 'halp'])
        pattern = re.compile(f'^(?:{tokens})$')

        super().__init__(name='help',
                         pattern=pattern,
                         help_text=help_text)

    def respond(self, slack_client, message, matches):
        send(slack_client, message['channel'], 'pong')

    def help_command(self, channel):
        help_header = HAI_DOMO
        help_text_list = map(lambda c: c.help(self.respond_tokens[0]), self.registered_commands)
        help_text_list = list(text for text in help_text_list if text)

        separator = '\n' + ':sparkles:' * 5 + '\n'

        help_commands = help_header + '\n\n' + separator.join(help_text_list)
        return self.sc.api_call("chat.postMessage",
                                channel=channel,
                                text=help_commands,
                                as_user=True)
