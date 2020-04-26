import re

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter


class PingCommand(SlackCommand):
    """usage: {bot} ping - respond with pong"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter):
        if not bot.addressed_by(message):
            return

        if bot.understands(message, with_pattern=re.compile('ping$', re.I)):
            bot.reply(message, 'pong')
            return

        if bot.understands(message, with_pattern=re.compile('bing$', re.I)):
            bot.reply(message, 'BONG', create_thread=True)
            return
