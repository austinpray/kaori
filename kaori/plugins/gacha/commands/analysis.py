import re
from tempfile import TemporaryFile
from typing import List, Dict

from typing.io import IO

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter
from kaori.plugins.gacha.analysis import rarity_histogram, get_rarity_dist, natures_heatmap, get_nature_matrix
from kaori.plugins.gacha.engine.core.card import Card as GameCard
from kaori.plugins.gacha.tui import card_stats_blocks
from kaori.skills import DB
from kaori.plugins.gacha.models.Card import get_game_cards


def generate_report_charts(game_cards: List[GameCard]) -> Dict[str, IO]:
    rarity = TemporaryFile()

    hist = rarity_histogram(get_rarity_dist(game_cards))

    hist.savefig(rarity)

    rarity.seek(0)

    natures = TemporaryFile()

    heatmap = natures_heatmap(get_nature_matrix(game_cards))

    heatmap.savefig(natures)

    natures.seek(0)

    return {
        'rarity': rarity,
        'natures': natures,
    }


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

            game_cards = get_game_cards(session)

            if not game_cards:
                bot.reply(message, "No cards", create_thread=True)
                return

        bot.reply(message,
                  blocks=card_stats_blocks(card_total=len(game_cards)),
                  create_thread=True)

        report = generate_report_charts(game_cards)

        bot.client.api_call(
            'files.upload',
            channels=message.channel,
            thread_ts=message.ts,
            filename='rarity.png',
            file=report['rarity'])

        bot.client.api_call(
            'files.upload',
            channels=message.channel,
            thread_ts=message.ts,
            filename='natures.png',
            file=report['natures'])
