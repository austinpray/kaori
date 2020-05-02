from typing import Dict, Tuple, Union

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


Number = Union[int, float]


def linear_scale(x: Number,
                 x_range: Tuple[Number, Number],
                 target_range: Tuple[Number, Number]) -> Number:
    """
    https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)
    """

    x_min = min(x_range)
    x_max = max(x_range)

    if not x_min <= x <= x_max:
        raise ValueError(f'{x} is not between {x_min} and {x_max}')

    a = min(target_range)
    b = max(target_range)
    return a + (x - x_min) * (b - a) / (x_max - x_min)
