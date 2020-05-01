from enum import unique, Enum


@unique
class StatName(Enum):
    HP = 'HP'
    EVA = 'EVA'
    ARMOR = 'ARMOR'
    DMG = 'DMG'
    CRIT = 'CRIT'
    SPEED = 'SPEED'


@unique
class RarityName(Enum):
    S = 'S'
    A = 'A'
    B = 'B'
    C = 'C'
    F = 'F'


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


class Nature:
    def __init__(self,
                 name: NatureName,
                 boosts: StatName,
                 inhibits: StatName) -> None:
        self.name = name
        self.boosts = boosts
        self.inhibits = inhibits

class CombatPower:
    pass