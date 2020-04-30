from enum import unique, Enum


@unique
class StatName(Enum):
    HP = 'HP'
    EVA = 'EVA'
    ARMOR = 'ARMOR'
    DMG = 'DMG'
    CRIT = 'CRIT'
    SPEED = 'SPEED'


class Rarity:

    def __init__(self, name: str, budget: int, split: int) -> None:
        self.name = name
        self.budget = budget
        self.split = split


class Nature:
    def __init__(self,
                 name: str,
                 boosts: StatName,
                 inhibits: StatName) -> None:
        self.name = name
        self.boosts = boosts
        self.inhibits = inhibits
