#!/usr/bin/env python3

from kaori.plugins.gacha.engine import *

matt_morg = {
    'name': "Matt Morgan",
    'rarity': S,
    'natures': (cursed, clown),
    'nature_values': {
        stupid: 1,
        baby: 1,
        clown: 6,
        horny: 3,
        cursed: 7,
        feral: 2,
        # stupid: 1,
        # baby: 1,
        # clown: 10,
        # horny: 1,
        # cursed: 6,
        # feral: 1,
    }
}

kim_jong_un_lil_sis = {
    'name': "Kim Jong Un's Little Sister",
    'rarity': S,
    'natures': (baby, horny),
    'nature_values': {
        stupid:	3,
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
        matt_morg,
        kim_jong_un_lil_sis,
        tlp
    ]

    for card in cards:
        assert sum(card['nature_values'].values()) == rarities[card['rarity']].budget
        print(f"------------")
        print(f"{card['name']} ({card['rarity']}-tier {' '.join((str(n) for n in card['natures']))})")
        print(f"## Nature")
        for k, v in card['nature_values'].items():
            print(f"{k}: {v}")
        print(f"## Stats")
        print(f"------------")
        for stat in [HP, EVA, ARMOR, DMG, CRIT, SPEED]:
            print(f"{stat}: {combat.calculate_stat(stat, card['nature_values'])}")
