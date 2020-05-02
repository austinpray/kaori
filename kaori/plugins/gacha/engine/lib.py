from enum import unique, Enum
from typing import Dict

from .utils import Number, linear_scale, nt_sigmoid


@unique
class StatName(Enum):
    HP = 'HP'
    EVA = 'EVA'
    ARMOR = 'ARMOR'
    DMG = 'DMG'
    CRIT = 'CRIT'
    SPEED = 'SPEED'

    def __str__(self):
        return self.value


@unique
class StatDisplay(Enum):
    number = 'number'
    percentage = 'percentage'


class Stat:

    def __init__(self, name: StatName,
                 i_min: Number,
                 i_max: Number,
                 display: StatDisplay = StatDisplay.number) -> None:
        self.name = name
        self.min = i_min
        self.max = i_max
        self.display = display


@unique
class RarityName(Enum):
    S = 'S'
    A = 'A'
    B = 'B'
    C = 'C'
    F = 'F'

    def __str__(self):
        return self.value


class Rarity:

    def __init__(self, name: RarityName, budget: int, split: int) -> None:
        self.name = name
        self.budget = budget
        self.split = split


@unique
class NatureName(Enum):
    stupid = 'stupid'
    baby = 'baby'
    clown = 'clown'
    horny = 'horny'
    cursed = 'cursed'
    feral = 'feral'

    def __str__(self):
        return self.value


class Nature:
    def __init__(self,
                 name: NatureName,
                 boosts: StatName,
                 inhibits: StatName) -> None:
        self.name = name
        self.boosts = boosts
        self.inhibits = inhibits


class Combat:
    def __init__(self,
                 rarities: Dict[RarityName, Rarity],
                 stats: Dict[StatName, Stat],
                 natures: Dict[NatureName, Nature]) -> None:
        self.rarities = rarities
        self.stats = stats
        self.natures = natures
        self.min_nature_value = 1
        self.max_nature_value = find_max_nature_value(rarities)

    def calculate_stat(self, stat: StatName, nature_values: Dict[NatureName, int]) -> Number:
        target_stat = self.stats[stat]

        natures = self.natures.values()
        booster = next((n.name for n in natures if n.boosts == stat))
        inhibitor = next((n.name for n in natures if n.inhibits == stat))

        booster_value = nature_values[booster]
        inhibitor_value = nature_values[inhibitor]

        # individually tunable stats
        if stat == HP:
            sensitivity = 0.95
        elif stat == EVA:
            sensitivity = 0.95
        else:
            sensitivity = 0.95

        tuner = linear_scale(booster_value / inhibitor_value,
                             (
                                 self.min_nature_value / self.max_nature_value,
                                 self.max_nature_value / self.min_nature_value
                             ),
                             (-sensitivity, sensitivity))

        value = linear_scale(booster_value,
                             (self.min_nature_value, self.max_nature_value),
                             (0, 1))

        return linear_scale(nt_sigmoid(tuner, value), (0, 1), (target_stat.min, target_stat.max))


def find_max_nature_value(rarities: Dict[RarityName, Rarity]) -> int:
    max_value = 0
    for rarity in rarities.values():
        rarity_max = rarity.budget - rarity.split - 4
        max_value = max(
            rarity_max,
            max_value
        )
    return max_value


HP = StatName.HP
EVA = StatName.EVA
ARMOR = StatName.ARMOR
DMG = StatName.DMG
CRIT = StatName.CRIT
SPEED = StatName.SPEED

S = RarityName.S
A = RarityName.A
B = RarityName.B
C = RarityName.C
F = RarityName.F

stupid = NatureName.stupid
baby = NatureName.baby
clown = NatureName.clown
horny = NatureName.horny
cursed = NatureName.cursed
feral = NatureName.feral
