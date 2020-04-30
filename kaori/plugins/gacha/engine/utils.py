from typing import Dict

from .lib import Rarity


def find_max_nature_value(rarities: Dict[str, Rarity]) -> int:
    max_value = 0
    for rarity in rarities.values():
        rarity_max = rarity.budget - rarity.split - 4
        max_value = max(
            rarity_max,
            max_value
        )
    return max_value
