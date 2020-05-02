#!/usr/bin/env python3

import arrow

from kaori.plugins.gacha.engine import *

balanced_S = {
    'name': "Balanced S",
    'rarity': S,
    'natures': (stupid, horny),
    'nature_values': {
        stupid: 6,
        baby: 2,
        clown: 2,
        horny: 6,
        cursed: 2,
        feral: 2,
    }
}

balanced_A = {
    'name': "Balanced A",
    'rarity': S,
    'natures': (stupid, horny),
    'nature_values': {
        stupid: 5,
        baby: 3,
        clown: 3,
        horny: 5,
        cursed: 2,
        feral: 2,
    }
}

balanced_B = {
    'name': "Balanced B",
    'rarity': B,
    'natures': (stupid, horny),
    'nature_values': {
        stupid: 4,
        baby: 3,
        clown: 3,
        horny: 4,
        cursed: 3,
        feral: 2,
    }
}

balanced_C = {
    'name': "Balanced C",
    'rarity': C,
    'natures': (stupid, horny),
    'nature_values': {
        stupid: 3,
        baby: 3,
        clown: 3,
        horny: 3,
        cursed: 2,
        feral: 2,
    }
}

balanced_F = {
    'name': "Balanced F",
    'rarity': F,
    'natures': (stupid, horny),
    'nature_values': {
        stupid: 2,
        baby: 2,
        clown: 2,
        horny: 2,
        cursed: 1,
        feral: 1,
    }
}





hp_no_invest = {
    'name': "Baseline HP with no investment",
    'rarity': B,
    'natures': (cursed, clown),
    'nature_values': {
        stupid: 1,
        baby: 1,
        clown: 6,
        horny: 4,
        cursed: 4,
        feral: 3,
    }
}

low_hp = {
    'name': "Lowest Possible HP in the game",
    'rarity': B,
    'natures': (horny, baby),
    'nature_values': {
        stupid: 1,
        baby: 11,
        clown: 1,
        horny: 4,
        cursed: 1,
        feral: 1,
    }
}

high_hp = {
    'name': "Highest Possible HP in the game",
    'rarity': B,
    'natures': (stupid, horny),
    'nature_values': {
        stupid: 11,
        baby: 1,
        clown: 1,
        horny: 4,
        cursed: 1,
        feral: 1,
    }
}

mid_hp = {
    'name': "Middle HP example",
    'rarity': B,
    'natures': (stupid, feral),
    'nature_values': {
        stupid: 5,
        baby: 1,
        clown: 1,
        horny: 7,
        cursed: 1,
        feral: 4,
    }
}

unlucky_hp = {
    'name': "Unlucky HP example",
    'rarity': B,
    'natures': (stupid, feral),
    'nature_values': {
        stupid: 5,
        baby: 2,
        clown: 1,
        horny: 6,
        cursed: 1,
        feral: 4,
    }
}

really_unlucky_hp = {
    'name': "Really Unlucky HP example",
    'rarity': B,
    'natures': (stupid, feral),
    'nature_values': {
        stupid: 5,
        baby: 3,
        clown: 1,
        horny: 5,
        cursed: 1,
        feral: 4,
    }
}

lucky_hp = {
    'name': "Lucky HP example",
    'rarity': B,
    'natures': (stupid, feral),
    'nature_values': {
        stupid: 6,
        baby: 1,
        clown: 1,
        horny: 6,
        cursed: 1,
        feral: 4,
    }
}

really_lucky_hp = {
    'name': "Really Lucky HP example",
    'rarity': B,
    'natures': (stupid, feral),
    'nature_values': {
        stupid: 7,
        baby: 1,
        clown: 1,
        horny: 5,
        cursed: 1,
        feral: 4,
    }
}

matt_morg = {
    'name': "Matt Morgan",
    'rarity': S,
    'natures': (cursed, clown),
    'nature_values': {
        stupid: 1,
        baby: 6,
        clown: 3,
        horny: 1,
        cursed: 7,
        feral: 2,
    }
}

kim_jong_un_lil_sis = {
    'name': "Kim Jong Un's Little Sister",
    'rarity': S,
    'natures': (horny, baby),
    'nature_values': {
        stupid: 3,
        baby: 6,
        clown: 1,
        horny: 7,
        cursed: 2,
        feral: 1
    }
}

tlp = {
    'name': "TLP",
    'rarity': C,
    'natures': (horny, feral),
    'nature_values': {
        stupid: 1,
        baby: 2,
        clown: 3,
        horny: 5,
        cursed: 2,
        feral: 3
    }
}


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
        'HP Simulations': [
            low_hp,
            really_unlucky_hp,
            unlucky_hp,
            mid_hp,
            lucky_hp,
            really_lucky_hp,
            high_hp,
            hp_no_invest,
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
