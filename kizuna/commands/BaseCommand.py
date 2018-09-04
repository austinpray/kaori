import re
from abc import ABC, abstractmethod
from io import StringIO

from kizuna.utils import db_session_scope


class BaseCommand(ABC):
    @abstractmethod
    def __init__(self, name, pattern, help_text='', is_at=True, db_session_maker=None) -> None:
        self.name = name
        self.is_at = is_at
        self.help_text = help_text
        self.pattern = re.compile(pattern, re.IGNORECASE) if isinstance(pattern, str) else pattern
        self.db_session_maker = db_session_maker

    def db_session_scope(self):
        return lambda: db_session_scope(self.db_session_maker)

    def help(self, bot_name):
        return self.help_text.replace("{bot}", bot_name)

    @staticmethod
    def add_help_command(parser):
        parser.add_argument('-h',
                            '--help',
                            action='store_true',
                            dest='help',
                            help='show this help message and exit')

    def set_help_text(self, parser):
        help_text_capture = StringIO()
        parser.print_help(file=help_text_capture)
        help_text = help_text_capture.getvalue()
        help_text = help_text.replace('usage: ', '')
        self.help_text = help_text

    @abstractmethod
    def respond(self, slack_client, message, matches):
        pass

    def maybe_respond(self, slack_client, message):
        match = self.pattern.match(message['text'])
        if bool(match):
            return self.respond(slack_client, message, match.groups())
