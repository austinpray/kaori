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
    output_strs = []
    output_strs.append(f"## Simulator Results: {arrow.utcnow()}")
    output_strs.append(f"### Game Facts")
    output_strs.append(f"{combat_strat.__class__.__name__} combat strategy")
    output_strs.append(trim_doc(combat_strat.__doc__))
    output_strs.append(f"Nature values range from {combat_strat.min_nature_value} to {combat_strat.max_nature_value}")
    output_strs.append(f"### Cards")
    for name, cards in card_groups.items():
        output_strs.append(f"<details><summary>{name}</summary>" if raw else "")
        card: Card
        for card in cards:
            output_strs.append(card.to_markdown())
        output_strs.append(f"</details>" if raw else "")

    output = "\n".join(output_strs)
    if raw:
        print(output)
    else:
        formatted = mdv.main(output, theme="960.847")
        print(formatted)
