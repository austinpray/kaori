#!/usr/bin/env python3

from kaori.plugins.gacha.engine import *

s_card = {
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
    }
}

if __name__ == '__main__':
    cards = [
        s_card
    ]

    for card in cards:
        print(f"------------")
        print(f"{card['name']} ({card['rarity']}-tier {' '.join((str(n) for n in card['natures']))})")
        print(f"## Nature")
        for k, v in card['nature_values'].items():
            print(f"{k}: {v}")
        print(f"## Stats")
        print(f"------------")
        for stat in [HP, EVA, ARMOR, DMG, CRIT, SPEED]:
            print(f"{stat}: {combat.calculate_stat(stat, card['nature_values'])}")
