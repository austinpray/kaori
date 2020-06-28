import re
from argparse import REMAINDER

from kaori.support.slacktools.arguments import SlackArgumentParserException, SlackArgumentParser

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter
from kaori.support.strings import random_insult

clap_parser = SlackArgumentParser(prog='kaori clap', description='obnoxiously clap', add_help=False)
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

clap_parser.add_help_argument()


class ClapCommand(SlackCommand):
    """usage: {bot} clap TEXT - adds obnoxious claps between each word in TEXT"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter):
        if not bot.addressed_by(message):
            return

        match = bot.understands(message, with_pattern=re.compile('clap (.*)'))

        if not match:
            return

        try:
            args = clap_parser.parse_args(match.group(1).split())
        except SlackArgumentParserException as err:
            # lol commented out for max sass
            # send(str(err))
            return bot.respond(message, random_insult())

        if args.help:
            return bot.respond(message, clap_parser.get_help())

        if not args.message:
            return bot.respond(message, random_insult())

        new_message = ' {} '.format(args.separator).join(args.message)

        if args.at:
            new_message = '{} {}'.format(args.at, new_message)

        bot.respond(message, new_message)
