import re

from kizuna.adapters.slack import SlackCommand, SlackMessage, SlackAdapter


class PingCommand(SlackCommand):
    """usage: {bot} ping - respond with pong"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter):
        if bot.addressed_by(message) and re.compile('.* ping$', re.I).match(message.text):
            bot.reply(message, 'pong')
