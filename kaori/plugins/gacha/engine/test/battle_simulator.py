import copy
from random import random
from typing import Optional

from . import cards as card_pool
from .utils import find_card
from .. import *
from .. import Card


class BattleResult:

    def __init__(self,
                 winner: Card,
                 loser: Card,
                 turns: int) -> None:
        self.turns = turns
        self.loser = loser
        self.winner = winner


def run_battle_simulator(card_a,
                         card_b,
                         debug: bool = False,
                         interactive: bool = False,
                         print_header: bool = True) -> Optional[BattleResult]:
    card_a: Card = find_card(card_pool, card_a)
    card_b: Card = find_card(card_pool, card_b)

    for card in [card_a, card_b]:
        card.is_valid_card()

    print()

    if print_header:
        print(card_a.title)
        print("VS")
        print(card_b.title)
        print()

        print(card_a.to_markdown())
        print(card_b.to_markdown())

    if Card.detect_standoff(card_a, card_b, debug=False):
        print(f"These two cards could go at it all day and not harm eachother due to armor, dmg, etc.")
        print(f"They agree to be friends instead of fighting.")
        return None

    cards = sorted([card_a, card_b], key=lambda card: -card.speed)
    first, second = cards

    print(f"{first.name} goes first because of higher speed. {first.speed} vs {second.speed}")

    winner = None
    loser = None
    turn = 0

    while card_a.current_hp > 0 and card_b.current_hp > 0:
        if turn > 100:
            raise RuntimeError('This battle is taking too long...')

        current_card = cards[turn % len(cards)]
        target_card = cards[(turn + 1) % len(cards)]
        print(f"{current_card.name} is attacking")
        # evasion check
        if random() < target_card.evasion:
            print(f"**{target_card.name} dodged the attack**")
            turn += 1
            continue

        crit_multiplier = 1
        # crit
        if random() < current_card.crit:
            crit_multiplier = CRIT_MULTIPLIER
            print(f"**{current_card.name} hit a crit!**")

        damage = current_card.attack_damage(target_card, crit_multiplier=crit_multiplier, debug=debug)
        print(f"{current_card.name} will hit {target_card.name} for {damage}!")
        target_card.accept_damage(damage)

        if target_card.current_hp < 1:
            print(f"{target_card.name} was killed!!")
            winner = current_card
            loser = target_card
            break
        else:
            print(f"{target_card.name} has {target_card.current_hp} HP left")

        turn += 1

    print("battle over")
    br = BattleResult(winner=copy.deepcopy(winner), loser=copy.deepcopy(loser), turns=turn + 1)
    for card in cards:
        card.reset_hp()
    return br
