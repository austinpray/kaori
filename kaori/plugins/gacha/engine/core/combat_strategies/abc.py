from abc import ABC, abstractmethod

from ..core import *


class CombatStrategyABC(ABC):

    def __init__(self,
                 rarities: Dict[RarityName, Rarity],
                 stats: Dict[StatName, Stat],
                 natures: Dict[NatureName, Nature],
                 crit_multiplier: int) -> None:
        self.rarities = rarities
        self.stats = stats
        self.natures = natures
        self.min_nature_value = 1
        self.max_nature_value = find_max_nature_value(rarities)
        self.crit_multiplier = crit_multiplier

    @abstractmethod
    def calculate_stat(self,
                       stat: StatName,
                       nature_values: Dict[NatureName, int]) -> Number:
        ...
