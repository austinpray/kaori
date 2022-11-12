from enum import unique, Enum
from typing import Dict

from ..utils import Number


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

    def __lt__(self, other):
        return self.value < other.value

    @classmethod
    def to_regex(cls) -> str:
        return '|'.join([str(n) for n in cls])


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

    @classmethod
    def to_regex(cls) -> str:
        return '|'.join([str(n) for n in cls])


class Nature:
    def __init__(self,
                 name: NatureName,
                 boosts: StatName,
                 inhibits: StatName) -> None:
        self.name = name
        self.boosts = boosts
        self.inhibits = inhibits


HP = StatName.HP
EVA = StatName.EVA
ARMOR = StatName.ARMOR
DMG = StatName.DMG
CRIT = StatName.CRIT
SPEED = StatName.SPEED

integer_stats = {HP, ARMOR, DMG}
rounded_stats = {EVA, CRIT}
rounded_stats_ndigits = 2

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

_noun_natures = {baby, clown}
_adj_natures = {stupid, horny, cursed, feral}


def humanize_nature(*args: NatureName) -> str:
    nouns = [str(n) for n in set(args).intersection(_noun_natures)]
    adjectives = [str(n) for n in set(args).intersection(_adj_natures)]
    natures_str = [str(n) for n in args]

    # all adjectives
    if len(nouns) == 0:
        return ' and '.join(natures_str)

    # all nouns
    if len(adjectives) == 0:
        return ' '.join(natures_str)

    return ' '.join([*adjectives, *nouns])


def find_max_nature_value(rarities: Dict[RarityName, Rarity]) -> int:
    max_value = 0
    for rarity in rarities.values():
        rarity_max = rarity.budget - rarity.split - 4
        max_value = max(
            rarity_max,
            max_value
        )
    return max_value
