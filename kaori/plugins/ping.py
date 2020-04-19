import re

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter


class PingCommand(SlackCommand):
    """usage: {bot} ping - respond with pong"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter):
        if bot.addressed_by(message) and bot.understands(message, with_pattern=re.compile('ping$', re.I)):
            bot.reply(message, 'pong')
