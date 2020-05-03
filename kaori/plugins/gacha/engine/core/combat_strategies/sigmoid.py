from .abc import CombatStrategyABC
from ..core import *
from ...utils import linear_scale, nt_sigmoid


class SigmoidV1(CombatStrategyABC):
    """
    - Natures can boost and inhibit certain stats
    - Stat values lie on a normalized tunable sigmoid curve
    """

    def __init__(self,
                 rarities: Dict[RarityName, Rarity],
                 stats: Dict[StatName, Stat],
                 natures: Dict[NatureName, Nature],
                 crit_multiplier: int,
                 stat_curvatures: Dict[StatName, Number]) -> None:
        super().__init__(rarities, stats, natures, crit_multiplier)
        self.stat_curvatures = stat_curvatures

    def calculate_stat(self,
                       stat: StatName,
                       nature_values: Dict[NatureName, int]) -> Number:
        target_stat = self.stats[stat]

        natures = self.natures.values()
        booster = next((n.name for n in natures if n.boosts == stat))
        inhibitor = next((n.name for n in natures if n.inhibits == stat))

        booster_value = nature_values[booster]
        inhibitor_value = nature_values[inhibitor]

        inhibition_factor = linear_scale(booster_value / inhibitor_value,
                                         (
                                             self.max_nature_value / self.min_nature_value,
                                             self.min_nature_value / self.max_nature_value,
                                         ),
                                         (0, 0.5))

        boost = linear_scale(booster_value,
                             (self.max_nature_value, self.min_nature_value),
                             (0, 0.5))

        return linear_scale(nt_sigmoid(self.stat_curvatures[stat], inhibition_factor + boost),
                            (0, 1),
                            (target_stat.min, target_stat.max))
