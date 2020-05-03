from . import meme_cards
from .. import *


def run_battle_simulator(card_a,
                         card_b,
                         debug: bool = False,
                         interactive: bool = False):
    card_a: Card = getattr(meme_cards, card_a)
    card_b: Card = getattr(meme_cards, card_b)

    print(card_a.to_markdown())
    print(card_b.to_markdown())

    pass
