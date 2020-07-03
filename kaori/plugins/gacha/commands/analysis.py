import re
from tempfile import TemporaryFile
from typing import List, Any

from kaori.plugins.users import User

from kaori.plugins.gacha.models.Card import Card

from kaori.plugins.gacha.engine.core.card import Card as GameCard

from kaori.skills import DB

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter
from kaori.plugins.gacha.analysis import rarity_histogram, get_rarity_dist, natures_heatmap, get_nature_matrix
from kaori.plugins.gacha.tui import card_stats_blocks


class CardStatsCommand(SlackCommand):
    """usage: {bot} card stats"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB):
        if not bot.addressed_by(message):
            return

        show_card_pattern = '|'.join([
            'cards? (?:stats|statistics)'
        ])
        if not bot.understands(message, with_pattern=re.compile(show_card_pattern, re.I)):
            return

        with db.session_scope() as session:

            cards = session.query(Card) \
                .filter(Card.published == True) \
                .all()

            if not cards:
                bot.reply(message, "No cards", create_thread=True)
                return

            game_cards: List[GameCard] = [card.engine for card in cards]

        bot.reply(message,
                  blocks=card_stats_blocks(card_total=len(game_cards)),
                  create_thread=True)

        t = TemporaryFile()

        hist = rarity_histogram(get_rarity_dist(game_cards))

        hist.savefig(t)

        t.seek(0)

        bot.client.api_call(
            'files.upload',
            channels=message.channel,
            thread_ts=message.ts,
            filename='rarity.png',
            file=t)

        t = TemporaryFile()

        heatmap = natures_heatmap(get_nature_matrix(game_cards))

        heatmap.savefig(t)

        t.seek(0)

        bot.client.api_call(
            'files.upload',
            channels=message.channel,
            thread_ts=message.ts,
            filename='natures.png',
            file=t)
