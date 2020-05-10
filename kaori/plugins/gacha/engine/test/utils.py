from copy import deepcopy
from random import choice
from typing import List, Dict

from ..core import Card


def collect_cards(module) -> Dict[str, Card]:
    card_variables: List[Card] = [
        getattr(module, var_name) for var_name in
        dir(module) if isinstance(getattr(module, var_name), Card)
    ]
    return {card.slug: card for card in card_variables}


def find_card(module, search: str) -> Card:
    available_cards = collect_cards(module)

    if search.lower() == 'random':
        return deepcopy(choice(list(available_cards.values())))

    search_slug = Card.sluggify_name(search)
    if search_slug in available_cards:
        return deepcopy(available_cards[search_slug])

    for slug, card in available_cards.items():
        if slug.startswith(search_slug):
            return deepcopy(card)

    raise ValueError(f'cannot find a card for {search}')
