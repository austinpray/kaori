from typing import Dict, Union, Tuple

import arrow

from .balanced_cards import *
from .dmg_cards import *
from .hp_cards import *
from .meme_cards import *
from .. import NatureName, RarityName


def run_card_simulator():
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

    print(f"## Simulator Results: {arrow.utcnow()}")
    print()
    print(f"### Game Facts")
    print()
    print(f"Nature values range from {combat.min_nature_value} to {combat.max_nature_value}")
    print()
    print(f"### Cards")
    print()
    for name, cards in card_groups.items():
        print(f"<details><summary>{name}</summary>")
        print()
        card: Card
        for card in cards:
            print(card.to_markdown())
        print(f"</details>")
        print()
