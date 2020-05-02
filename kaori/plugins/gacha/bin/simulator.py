#!/usr/bin/env python3

import arrow

from kaori.plugins.gacha.engine.test.balanced_cards import *
from kaori.plugins.gacha.engine.test.dmg_cards import *
from kaori.plugins.gacha.engine.test.hp_cards import *
from kaori.plugins.gacha.engine.test.meme_cards import *


def render_card_md(card, combat):
    nv_sum = sum(card['nature_values'].values())
    budget = rarities[card['rarity']].budget

    assert nv_sum == budget, \
        f"'**ERROR:** {card['name']}' {nv_sum} does not square with budget {budget}"

    print(f"#### {card['name']} ({card['rarity']}-tier {' '.join((str(n) for n in card['natures']))})")
    print()
    print("Nature | Value | Stat | Value ")
    print("------ | --- | ---- | --- ")
    for k, v in card['nature_values'].items():
        print(' | '.join([
            f"**{k}**",
            str(v),
            f"**{combat.natures[k].boosts}**",
            str(combat.calculate_stat(combat.natures[k].boosts, card['nature_values'])),
        ]))
    print()


if __name__ == '__main__':
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
        for card in cards:
            render_card_md(card, combat=combat)
        print(f"</details>")
        print()
