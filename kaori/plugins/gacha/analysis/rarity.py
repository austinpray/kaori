from typing import List, Dict
import matplotlib.pyplot as plt

from pandas import DataFrame

from kaori.plugins.gacha.engine.core import Card as GameCard, RarityName

import seaborn as sns

_dist = Dict[RarityName, int]


def get_rarity_dist(cards: List[GameCard]) -> _dist:
    hist = {
        r: 0 for r in RarityName
    }
    for c in cards:
        hist[c.rarity] += 1

    return hist


def rarity_histogram(dist: _dist):
    df = DataFrame([[rarity, count] for rarity, count in dist.items()], columns=['rarity', 'count'])
    fig, ax = plt.subplots()
    bar = sns.barplot(x='rarity', y='count', data=df, ax=ax)

    bar.set_title("Rarity Counts")

    return bar.get_figure()
