from . import meme_cards
from .. import *


def run_battle_simulator(card_a,
                         card_b,
                         debug: bool = False,
                         interactive: bool = False):
    card_a: Card = getattr(meme_cards, card_a)
    card_b: Card = getattr(meme_cards, card_b)

    print()
    print(card_a.title)
    print("VS")
    print(card_b.title)
    print()

    print(card_a.to_markdown())
    print(card_b.to_markdown())

    first = max([card_a, card_b], key=lambda c: c.speed)
    second = min([card_a, card_b], key=lambda c: c.speed)

    print(f"{first.name} goes first because of higher speed. {first.speed} vs {second.speed}")



    turn = 1
    while card_a.current_hp > 0 and card_b.current_hp > 0:
        break
        if turn > 1000:
            break

        print(f"Turn {1}")


    print("battle over")

