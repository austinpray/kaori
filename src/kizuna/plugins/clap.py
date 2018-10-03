import re
from argparse import REMAINDER
from slacktools.arguments import SlackArgumentParserException, SlackArgumentParser

from kizuna.adapters.slack import SlackCommand, SlackMessage, SlackAdapter

clap_parser = SlackArgumentParser(prog='kizuna clap', description='obnoxiously clap', add_help=False)
clap_parser.add_argument('-s',
                         '--separator',
                         dest='separator',
                         default=':clap:',
                         help='defaults to :clap:')

clap_parser.add_argument('-a',
                         '--at',
                         dest='at',
                         metavar='PERSON',
                         help='a user to send this message to')

clap_parser.add_argument('message',
                         metavar='MESSAGE',
                         nargs=REMAINDER,
                         help='the message to clappify')


class ClapCommand(SlackCommand):
    """usage: {bot} clap TEXT - adds obnoxious claps between each word in TEXT"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter):
        if not bot.addressed_by(message):
            return

        match = bot.understands(message, with_pattern=re.compile(''))

        try:
            args = clap_parser.parse_args(message.text.split(' '))
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
