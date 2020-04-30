from .lib import Rarity, Nature, StatName
from .utils import find_max_nature_value

HP = StatName.HP
EVA = StatName.EVA
ARMOR = StatName.ARMOR
DMG = StatName.DMG
CRIT = StatName.CRIT
SPEED = StatName.SPEED


HP_MAX = 100
EVA_MAX = 0.9
ARMOR_MAX = 10
DAMAGE_MAX = 100

CRIT_MAX = 0.9
CRIT_MULTIPLIER = 3

rarities = {
    r.name: r for r in
    [
        Rarity(name='S', budget=20, split=6),
        Rarity(name='A', budget=20, split=5),
        Rarity(name='B', budget=19, split=4),
        Rarity(name='C', budget=16, split=3),
        Rarity(name='F', budget=10, split=2),
    ]
}

min_nature_value = 1
max_nature_value = find_max_nature_value(rarities)

stats = {
    name: (min_value, max_value) for (name, min_value, max_value) in
    [
        (HP, 1, HP_MAX),
        (EVA, 0, EVA_MAX),
        (ARMOR, 0, ARMOR_MAX),
        (DMG, 1, DAMAGE_MAX),
        (CRIT, 0, CRIT_MAX),
        (SPEED, 1, max_nature_value)
    ]
}

natures = {
    n.name: n for n in
    [
        Nature(name='stupid', boosts=HP, inhibits=SPEED),
        Nature(name='baby', boosts=EVA, inhibits=HP),
        Nature(name='clown', boosts=ARMOR, inhibits=EVA),
        Nature(name='horny', boosts=DMG, inhibits=ARMOR),
        Nature(name='cursed', boosts=CRIT, inhibits=DMG),
        Nature(name='feral', boosts=SPEED, inhibits=CRIT),
    ]
}
