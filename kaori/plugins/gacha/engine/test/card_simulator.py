from io import StringIO
import arrow
import mdv

from .balanced_cards import *
from .dmg_cards import *
from .hp_cards import *
from .meme_cards import *
from .. import Card
from ..utils import trim_doc


def run_card_simulator(raw=False):
    card_groups = {
        'Baselines': [
            hp_no_invest,
            dmg_no_invest,
        ],
        'HP Simulations': [
            low_hp,
            really_unlucky_hp,
            unlucky_hp,
            mid_hp,
            lucky_hp,
            really_lucky_hp,
            high_hp,
        ],
        'DMG Simulations': [
            low_dmg,
            really_unlucky_dmg,
            unlucky_dmg,
            mid_dmg,
            lucky_dmg,
            really_lucky_dmg,
            unlikely_dmg1,
            unlikely_dmg2,
            unlikely_dmg3,
            high_dmg,
        ],
        'Random Interesting Cards': [
            matt_morg,
            kim_jong_un_lil_sis,
            tlp,
        ],
        'Balanced Cards': [
            balanced_S,
            balanced_A,
            balanced_B,
            balanced_C,
            balanced_F,
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
