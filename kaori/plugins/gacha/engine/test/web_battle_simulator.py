import urllib.parse
from typing import List

import ujson

from . import cards as card_pool
from .utils import find_card
from .. import Card
from ..core.battle import Battle


def run_web_battle_simulator(card_a_name: str,
                             card_b_name: str,
                             repeat: int = 1,
                             out_format: str = None,
                             debug: bool = False,
                             interactive: bool = False) -> List[Battle]:
    results: List[Battle] = []
    card_a: Card = find_card(card_pool, card_a_name)
    card_b: Card = find_card(card_pool, card_b_name)

    for i in range(repeat):

        if not card_a.id:
            card_a.id = 1
        if not card_b.id:
            card_b.id = card_a.id + 1

        results.append(Battle(card_a=card_a, card_b=card_b).run())
        card_a.reset_hp()
        card_b.reset_hp()

    if not out_format:
        return results

    o = out_format
    if o.startswith('web'):
        for result in results:
            payload = ujson.dumps(result.serialize_min())
            if o == 'web_raw':
                print(payload)
                continue
            else:
                print('http://localhost:8080/battle/?in=' + urllib.parse.quote_plus(payload))
        else:
            raise RuntimeError(f"unknown output format '{out_format}'")

    return results
