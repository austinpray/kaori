from . import *
from .test.web_battle_simulator import run_web_battle_simulator

from .test.cards.hp_cards import low_hp, high_hp


def test_engine():
    assert find_max_nature_value(rarities) == 11
    assert int(combat_strat.calculate_stat(HP, low_hp.nature_values)) == 1
    assert int(combat_strat.calculate_stat(HP, high_hp.nature_values)) == 100

def test_battle():
    results = run_web_battle_simulator('balanced A', 'balanced A', repeat=1000)
    assert len(results) == 1000
    results = run_web_battle_simulator('balanced A', 'balanced F', repeat=1000)
    assert len(results) == 1000
