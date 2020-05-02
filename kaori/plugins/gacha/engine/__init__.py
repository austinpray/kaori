from .lib import *

HP_MAX = 100
EVA_MAX = 0.9
ARMOR_MAX = 10
DAMAGE_MAX = 100

stat_curvatures = {
    HP: 0, 
    EVA: 0,
    ARMOR: 0,
    DMG: 0,
    CRIT: 0,
    SPEED: 0,
}

CRIT_MAX = 0.9
CRIT_MULTIPLIER = 3

rarities = {
    r.name: r for r in
    [
        Rarity(name=S, budget=20, split=6),
        Rarity(name=A, budget=20, split=5),
        Rarity(name=B, budget=19, split=4),
        Rarity(name=C, budget=16, split=3),
        Rarity(name=F, budget=10, split=2),
    ]
}

stats = {
    stat.name: stat for stat in
    [
        Stat(name=HP, i_min=1, i_max=HP_MAX),
        Stat(name=EVA, i_min=0, i_max=EVA_MAX),
        Stat(name=ARMOR, i_min=0, i_max=ARMOR_MAX),
        Stat(name=DMG, i_min=1, i_max=DAMAGE_MAX),
        Stat(name=CRIT, i_min=0, i_max=CRIT_MAX),
        Stat(name=SPEED, i_min=1, i_max=100),
    ]
}

natures = {
    n.name: n for n in
    [
        Nature(name=stupid, boosts=HP, inhibits=SPEED),
        Nature(name=baby, boosts=EVA, inhibits=HP),
        Nature(name=clown, boosts=ARMOR, inhibits=EVA),
        Nature(name=horny, boosts=DMG, inhibits=ARMOR),
        Nature(name=cursed, boosts=CRIT, inhibits=DMG),
        Nature(name=feral, boosts=SPEED, inhibits=CRIT),
    ]
}

combat = Combat(rarities=rarities,
                stats=stats,
                natures=natures,
                stat_curvatures=stat_curvatures)
