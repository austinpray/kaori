#!/usr/bin/env python3

from kaori.plugins.gacha.engine import *

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

if __name__ == '__main__':
    cards = [
        low_hp,
        really_unlucky_hp,
        unlucky_hp,
        mid_hp,
        lucky_hp,
        really_lucky_hp,
        high_hp,
        matt_morg,
        kim_jong_un_lil_sis,
        tlp,
    ]

    print()

    for card in cards:
        nv_sum = sum(card['nature_values'].values())
        budget = rarities[card['rarity']].budget
        assert nv_sum == budget, \
            f"'{card['name']}' {nv_sum} does not square with budget {budget}"
        print(f"------------")
        print(f"{card['name']} ({card['rarity']}-tier {' '.join((str(n) for n in card['natures']))})")
        print(f"## Nature")
        for k, v in card['nature_values'].items():
            print(f"{k}: {v}")
        print(f"## Stats")
        for stat in [HP, EVA, ARMOR, DMG, CRIT, SPEED]:
            print(f"{stat}: {combat.calculate_stat(stat, card['nature_values'])}")
        print(f"------------")
        print()
