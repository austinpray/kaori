from __future__ import annotations

import sys
from io import StringIO
from typing import Tuple

from .combat_strategies import CombatStrategyABC
from .core import *


class Card:
    combat_strat: CombatStrategyABC = None

    def __init__(self,
                 name: str,
                 rarity: RarityName,
                 nature: Tuple[NatureName, NatureName],
                 **kwargs) -> None:

        if self.combat_strat is None:
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

    def accept_damage(self, value: int):
        self._current_hp -= value

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
        value = self.combat_strat.calculate_stat(name, self.nature_values)
        if name in integer_stats:
            return round(value)

        if name in rounded_stats:
            return round(value, rounded_stats_ndigits)

        return value

    def reset_hp(self):
        self._current_hp = self.max_hp

    def is_valid_card(self) -> bool:
        nv_sum = sum(self.nature_values.values())
        budget = self.combat_strat.rarities[self.rarity].budget
        assert nv_sum == budget, \
            f"'**ERROR:** {self.name}' {nv_sum} does not square with budget {budget}"

        return True

    @property
    def title(self):
        return f"{self.name} ({self.rarity}-tier {humanize_nature(*self.nature)})"

    @staticmethod
    def detect_standoff(a: Card, b: Card, debug: bool = False) -> bool:
        a_max_dmg = a.attack_damage(b,
                                    crit_multiplier=Card.combat_strat.crit_multiplier,
                                    debug=debug)
        b_max_dmg = b.attack_damage(a,
                                    crit_multiplier=Card.combat_strat.crit_multiplier,
                                    debug=debug)
        return max(a_max_dmg, b_max_dmg) == 0

    def to_markdown(self):
        out = StringIO()

        def p(x=None):
            return print(x, file=out) if x else print(file=out)

        p(f"#### {self.title}")
        p()
        p("Nature | Value | Stat | Value ")
        p("------ | --- | ---- | --- ")
        for k, v in self.nature_values.items():
            target_stat = self.combat_strat.natures[k].boosts
            stat = self._stat(target_stat)
            if target_stat in {EVA, CRIT}:
                stat = f"{round(stat * 100)}%"

            p(' | '.join([
                f"**{k}**",
                str(v),
                f"**{self.combat_strat.natures[k].boosts}**",
                str(stat),
            ]))
        p()

        return out.getvalue()

    @staticmethod
    def sluggify_name(name) -> str:
        return '-'.join(name.strip().split()).lower().encode('idna').decode('utf-8')

    @property
    def slug(self) -> str:
        return Card.sluggify_name(self.name)

    def attack_damage(self,
                      target: Card,
                      crit_multiplier: int = 1,
                      debug: bool = False) -> int:
        apply_crit = self.dmg * crit_multiplier
        apply_armor = apply_crit - target.armor
        rounded = round(apply_armor)
        dmg = max(0, rounded)
        if debug:
            print(
                f"[debug] Attack Calculation: "
                f"max(0, round({self.dmg} * {crit_multiplier}) - {target.armor}))",
                file=sys.stderr)
        return dmg
