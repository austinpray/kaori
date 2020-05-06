from __future__ import annotations
from enum import Enum, unique
from random import sample, random
from typing import List

from .card import Card
from .. import CRIT_MULTIPLIER


@unique
class TurnResult(Enum):
    standoff = 'S'
    evade = 'E'
    hit = 'H'
    kill = 'K'

    def __str__(self):
        return self.value


_standoff = TurnResult.standoff
_evade = TurnResult.evade
_hit = TurnResult.hit
_kill = TurnResult.kill


class Turn:

    def __init__(self,
                 attacker: Card,
                 defender: Card,
                 result: TurnResult) -> None:
        self.result = result
        self.defender = defender
        self.attacker = attacker
        self.dmg = 0
        self.crit = False

    def __str__(self) -> str:
        return f"{self.attacker.id}x{self.defender.id}_" \
               f"{str(self.result)}{self.dmg}_{int(self.crit)}"


class Battle:
    turns: List[Turn]

    def __init__(self,
                 card_a: Card,
                 card_b: Card) -> None:

        self.card_a = card_a
        self.card_b = card_b

        self.winner = None
        self.loser = None

        self.turns = []

        self.debug = False

    def run(self) -> Battle:
        a = self.card_a
        b = self.card_b

        if a.speed != b.speed:
            cards = sorted([a, b], key=lambda card: -card.speed)
        else:
            cards = sample([a, b], 2)

        first, second = cards

        if Card.detect_standoff(a, b, debug=self.debug):
            self.turns.append(Turn(attacker=first, defender=second, result=_standoff))
            return self

        while a.current_hp > 0 and b.current_hp > 0:
            turn = len(self.turns)
            if turn > 100:
                raise RuntimeError('This battle is taking too long...')

            attacker = cards[turn % len(cards)]
            defender = cards[(turn + 1) % len(cards)]

            turn = Turn(attacker=attacker, defender=defender, result=_hit)

            # evasion check
            if random() < defender.evasion:
                turn.result = _evade
                self.turns.append(turn)
                continue

            crit_multiplier = 1
            if random() < attacker.crit:
                crit_multiplier = CRIT_MULTIPLIER
                turn.crit = True

            turn.dmg = attacker.attack_damage(defender, crit_multiplier=crit_multiplier, debug=self.debug)
            defender.accept_damage(turn.dmg)

            if defender.current_hp < 1:
                turn.result = _kill
                self.turns.append(turn)
                self.winner = attacker
                self.loser = defender
                break

            self.turns.append(turn)

        return self

    def serialize_min(self):
        return {
            'a': self.card_a.serialize_min(),
            'b': self.card_b.serialize_min(),
            'turns': '~'.join([str(t) for t in self.turns])
        }
