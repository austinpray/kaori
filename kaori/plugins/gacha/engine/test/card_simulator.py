from io import StringIO

import arrow
import mdv

from .cards import *
from kaori.plugins.gacha.engine.test.cards.dmg_cards import dmg_no_invest
from kaori.plugins.gacha.engine.test.cards.hp_cards import hp_no_invest
from .utils import collect_cards
from .. import *
from ..utils import trim_doc


def run_card_simulator(raw=False):
    card_groups = {
        'Baselines': [
            hp_no_invest,
            dmg_no_invest,
        ],
        'HP Simulations': [
            *collect_cards(hp_cards).values(),
        ],
        'DMG Simulations': [
            *collect_cards(dmg_cards).values(),
        ],
        'Random Interesting Cards': [
            *collect_cards(meme_cards).values()
        ],
        'Balanced Cards': [
            *collect_cards(balanced_cards).values()
        ],
    }

    # validate cards
    for name, cards in card_groups.items():
        card: Card
        for card in cards:
            card.is_valid_card()

    out = StringIO()

    def p(x=None):
        return print(x, file=out) if x else print(file=out)

    p(f"## Simulator Results: {arrow.utcnow()}")
    p()
    p(f"### Game Facts")
    p(f"{combat_strat.__class__.__name__} combat strategy")
    p(trim_doc(combat_strat.__doc__))
    p()
    p(f"Nature values range from {combat_strat.min_nature_value} to {combat_strat.max_nature_value}")
    p()
    p(f"### Cards")
    p()
    for name, cards in card_groups.items():
        p(f"<details><summary>{name}</summary>" if raw else f"### {name}")
        p()
        card: Card
        for card in cards:
            p(card.to_markdown())
        p(f"</details>" if raw else "")
        p()

    if raw:
        print(out.getvalue())
    else:
        print(mdv.main(out.getvalue(), theme="960.847"))
