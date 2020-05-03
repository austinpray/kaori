from random import random

from . import meme_cards
from .. import *


def run_battle_simulator(card_a,
                         card_b,
                         debug: bool = False,
                         interactive: bool = False,
                         print_header: bool = True):
    card_a: Card = getattr(meme_cards, card_a)
    card_b: Card = getattr(meme_cards, card_b)

    print()

    if print_header:
        print(card_a.title)
        print("VS")
        print(card_b.title)
        print()

        print(card_a.to_markdown())
        print(card_b.to_markdown())

    cards = sorted([card_a, card_b], key=lambda card: -card.speed)
    first, second = cards

    print(f"{first.name} goes first because of higher speed. {first.speed} vs {second.speed}")

    turn = 0
    while card_a.current_hp > 0 and card_b.current_hp > 0:
        if turn > 1000:
            raise RuntimeError('This battle is taking too long...')

        current_card = cards[turn % len(cards)]
        target_card = cards[(turn + 1) % len(cards)]
        print(f"{current_card.name} is attacking")
        # evasion check
        if random() < target_card.evasion:
            print(f"{target_card.name} dodged the attack")
            turn += 1
            continue

        crit_multiplier = 1
        # crit
        if random() < current_card.crit:
            crit_multiplier = 3
            print(f"{current_card.name} hit a crit!")

        damage = current_card.attack_damage(target_card, crit_multiplier=crit_multiplier)
        print(f"{current_card.name} will hit {target_card.name} for {damage}!")
        target_card.accept_damage(damage)

        if target_card.current_hp < 1:
            print(f"{target_card.name} was killed!!")
        else:
            print(f"{target_card.name} has {target_card.current_hp} HP left")

        turn += 1

    print("battle over")
    for card in cards:
        card.reset_hp()
