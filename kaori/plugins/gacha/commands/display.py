import re

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter
from kaori.plugins.users import User
from kaori.skills import DB
from ..models.Card import Card
from ..tui import render_card, card_index_blocks


class CardDisplayCommand(SlackCommand):
    """usage: {bot} show card {name}"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB):
        if not bot.addressed_by(message):
            return

        show_card_pattern = '|'.join([
            '(?:get|show|find) card'
        ])
        show_card_pattern = f'(?:{show_card_pattern})'
        pattern = re.compile(f'{show_card_pattern} (.+)', re.I)
        search = bot.understands(message, with_pattern=pattern)

        if not search:
            return

        with db.session_scope() as session:

            card = Card.search_for_one(session, search[1])

            if not card:
                bot.reply(message, 'no card with that name', create_thread=True)
                return

            bot.reply(message, create_thread=True, **render_card(card))


class CardIndexCommand(SlackCommand):
    """usage: {bot} show cards"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB):
        if not bot.addressed_by(message):
            return

        show_card_pattern = '|'.join([
            '(?:get|gimme|show|find|list) ?(?:my|muh)? cardo?s'
        ])
        if not bot.understands(message, with_pattern=re.compile(show_card_pattern, re.I)):
            return

        with db.session_scope() as session:

            cards = session.query(Card) \
                .join(User) \
                .filter(User.slack_id == message.user) \
                .filter(Card.published == True) \
                .limit(10) \
                .all()

            if not cards:
                bot.reply(message, "You don't have any cards yet.", create_thread=True)
                return

            bot.reply(message, create_thread=True, blocks=card_index_blocks(cards))
