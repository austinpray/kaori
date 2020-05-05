from random import choice
from typing import List, Dict

from ..core import Card


def collect_cards(module) -> Dict[str, Card]:
    card_variables: List[Card] = [
        getattr(module, var_name) for var_name in
        dir(module) if isinstance(getattr(module, var_name), Card)
    ]
    return {card.slug: card for card in card_variables}


def find_card(module: object, search: str) -> Card:
    available_cards = collect_cards(module)

    if search.lower() == 'random':
        return choice(list(available_cards.values()))

    return available_cards[Card.sluggify_name(search)]
