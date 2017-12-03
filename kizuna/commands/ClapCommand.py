from kizuna.commands.Command import Command
from kizuna.strings import random_insult
from kizuna.SlackArgumentParser import SlackArgumentParser, SlackArgumentParserException

from argparse import REMAINDER


class ClapCommand(Command):
    def __init__(self) -> None:
        parser = SlackArgumentParser(prog='kizuna clap', description='obnoxiously clap', add_help=False)
        self.add_help_command(parser)

        parser.add_argument('-s',
                            '--separator',
                            dest='separator',
                            default=':clap:',
                            help='defaults to :clap:')

        parser.add_argument('-a',
                            '--at',
                            dest='at',
                            metavar='PERSON',
                            help='a user to send this message to')

        parser.add_argument('message',
                            metavar='MESSAGE',
                            nargs=REMAINDER,
                            help='the message to clappify')

        self.set_help_text(parser)
        self.parser = parser
        super().__init__('clap', 'clap (.*)', help_text=self.help_text, is_at=True)

    def respond(self, slack_client, message, matches):
        send = self.send_factory(slack_client, message['channel'])
        try:
            args = self.parser.parse_args(matches[0].split(' '))
        except SlackArgumentParserException as err:
            # lol commented out for max sass
            # send(str(err))
            return send(random_insult())

        if args.help:
            return send(self.help_text)

        if not args.message:
            return send(random_insult())

        new_message = ' {} '.format(args.separator).join(args.message)

        if args.at:
            new_message = '{} {}'.format(args.at, new_message)

        send(new_message)
