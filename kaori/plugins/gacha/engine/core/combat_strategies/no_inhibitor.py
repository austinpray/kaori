from .abc import CombatStrategyABC
from ..core import *
from ...utils import linear_scale


class NoInhibitorV0(CombatStrategyABC):
    """
    - Natures only boost
    - WIP: haven't tested this
    - TODO: @ridhoq needs to fill out his idea
    """

    def calculate_stat(self,
                       stat: StatName,
                       nature_values: Dict[NatureName, int]) -> Number:
        target_stat = self.stats[stat]

        natures = self.natures.values()
        booster = next((n.name for n in natures if n.boosts == stat))

        booster_value = nature_values[booster]

        return linear_scale(booster_value,
                            (self.min_nature_value, self.max_nature_value),
                            (target_stat.min, target_stat.max))
