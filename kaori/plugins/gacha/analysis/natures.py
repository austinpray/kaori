from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
from datetime import datetime
import itertools

from kaori.plugins.gacha.engine import NatureName

from kaori.plugins.gacha.engine.core import Card as GameCard
from pandas import DataFrame

import seaborn as sns

nature_matrix = Dict[Tuple[str, ...], int]


def _make_key(combo):
    return tuple(sorted(combo))


def _make_nature_dict() -> nature_matrix:
    combinations = itertools.combinations([str(n) for n in NatureName], 2)

    return {
        _make_key(combo): 0 for combo in combinations
    }


def get_nature_matrix(cards: List[GameCard]) -> nature_matrix:
    matrix = _make_nature_dict()

    for card in cards:
        key = _make_key((str(n) for n in card.nature))
        matrix[key] += 1

    return matrix


def natures_heatmap(matrix: nature_matrix, ts=datetime.now()):
    df = DataFrame([[*k, v] for k, v in matrix.items()], columns=['n1', 'n2', 'count'])
    fig, ax = plt.subplots()
    hm = sns.heatmap(df.pivot('n1', 'n2', 'count'), annot=True, ax=ax)

    hm.set_title(f'Nature Combinations Heatmap ({ts.strftime("%Y-%m-%d")})')

    return hm.get_figure()
