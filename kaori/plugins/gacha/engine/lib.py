from enum import unique, Enum
from typing import Dict, Tuple, List
from io import StringIO

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
                 natures: Dict[NatureName, Nature],
                 stat_curvatures: Dict[StatName, Number]) -> None:
        self.rarities = rarities
        self.stats = stats
        self.natures = natures
        self.min_nature_value = 1
        self.max_nature_value = find_max_nature_value(rarities)
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


class Card:
    combat: Combat = None

    def __init__(self,
                 name: str,
                 rarity: RarityName,
                 nature: Tuple[NatureName, NatureName],
                 **kwargs) -> None:

        if self.combat is None:
            raise RuntimeError('You need to set the initialize the combat class')

        self.name = name
        self.rarity = rarity
        self.nature = nature
        self.stupid = 1
        self.baby = 1
        self.clown = 1
        self.horny = 1
        self.cursed = 1
        self.feral = 1
        self._current_hp = None
        for name, value in kwargs.items():
            whitelist = [
                'stupid', 'baby', 'clown', 'horny', 'cursed', 'feral'
            ]
            if name in whitelist:
                setattr(self, name, value)

    def __repr__(self) -> str:
        return f"<Card name='{self.name}' " \
               f"natures='{humanize_nature(*self.nature)}' " \
               f"current_hp={self.current_hp}>"

    @property
    def nature_values(self):
        return {
            stupid: self.stupid,
            baby: self.baby,
            clown: self.clown,
            horny: self.horny,
            cursed: self.cursed,
            feral: self.feral,
        }

    @property
    def current_hp(self):
        if self._current_hp is None:
            self.reset_hp()

        return round(self._current_hp)

    @property
    def dmg(self):
        return self._stat(DMG)

    @property
    def speed(self):
        return self._stat(SPEED)

    @property
    def crit(self):
        return self._stat(CRIT)

    @property
    def armor(self):
        return self._stat(ARMOR)

    @property
    def evasion(self):
        return self._stat(EVA)

    @property
    def max_hp(self):
        return self._stat(HP)

    def _stat(self, name: StatName):
        value = self.combat.calculate_stat(name, self.nature_values)
        if name in _integer_stats:
            return round(value)

        if name in _rounded_stats:
            return round(value, _rounded_stats_ndigits)

        return value

    def reset_hp(self):
        self._current_hp = self.max_hp

    def is_valid_card(self) -> bool:
        nv_sum = sum(self.nature_values.values())
        budget = self.combat.rarities[self.rarity].budget
        assert nv_sum == budget, \
            f"'**ERROR:** {self.name}' {nv_sum} does not square with budget {budget}"

        return True

    @property
    def title(self):
        return f"{self.name} ({self.rarity}-tier {humanize_nature(*self.nature)})"

    def to_markdown(self):
        out = StringIO()

        def p(x=None):
            return print(x, file=out) if x else print(file=out)

        p(f"#### {self.title}")
        p()
        p("Nature | Value | Stat | Value ")
        p("------ | --- | ---- | --- ")
        for k, v in self.nature_values.items():
            target_stat = self.combat.natures[k].boosts
            stat = self._stat(target_stat)
            if target_stat in {EVA, CRIT}:
                stat = f"{round(stat*100)}%"

            p(' | '.join([
                f"**{k}**",
                str(v),
                f"**{self.combat.natures[k].boosts}**",
                str(stat),
            ]))
        p()

        return out.getvalue()


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

_integer_stats = {HP, ARMOR, DMG}
_rounded_stats = {EVA, CRIT}
_rounded_stats_ndigits = 2

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
