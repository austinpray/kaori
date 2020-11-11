import re

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter
from ..tui import price_blocks, help_blocks


class CardPriceCommand(SlackCommand):
    """usage: {bot} card prices - start card creation"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter):
        if not bot.addressed_by(message):
            return

        if not bot.understands(message, with_pattern=re.compile('card prices?[?]?$', re.I)):
            return

        res = bot.reply(message, text='Here are the current prices for creating cards:', blocks=price_blocks())
        if not res['ok']:
            print(res)


class CardHelpCommand(SlackCommand):
    """usage: {bot} card prices - start card creation"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter):
        if not bot.addressed_by(message):
            return

        asking_help = re.compile(r'(?:cards|gacha) ?(?:help|-h|--help)?', re.I)
        question = re.compile(r'(?:what|why|how|explain).+(?:cards?|gacha)', re.I)

        if not (bot.understands(message, with_pattern=asking_help) or
                bot.understands(message, with_pattern=question)):
            return

        bot.reply(message, blocks=help_blocks(), create_thread=True, reply_broadcast=True)
