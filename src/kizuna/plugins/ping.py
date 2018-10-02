import re

from kizuna.adapters.slack import SlackCommand, SlackMessage, SlackAdapter


class PingCommand(SlackCommand):
    """usage: {bot} ping - respond with pong"""

    @staticmethod
    def handle(message: SlackMessage, bot: SlackAdapter):
        if re.compile('ping$', re.I).match(message.text):
            bot.respond(message, 'pong')
