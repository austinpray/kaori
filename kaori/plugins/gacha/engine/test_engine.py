from . import *

from kaori.plugins.gacha.engine.test.card_simulator import low_hp, high_hp


def test_engine():
    assert find_max_nature_value(rarities) == 11
    assert int(combat.calculate_stat(HP, low_hp.nature_values)) == 1
    assert int(combat.calculate_stat(HP, high_hp.nature_values)) == 100
