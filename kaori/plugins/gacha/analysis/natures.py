from typing import List, Dict
import matplotlib.pyplot as plt
from datetime import datetime

from kaori.plugins.gacha.engine import NatureName

from kaori.plugins.gacha.engine.core import Card as GameCard
from pandas import DataFrame

import seaborn as sns

nature_matrix = Dict[NatureName, Dict[NatureName, int]]


def _make_nature_dict() -> nature_matrix:
    return {
        n: {
            n: 0 for n in NatureName
        } for n in NatureName
    }


def get_nature_matrix(cards: List[GameCard]) -> nature_matrix:
    matrix = _make_nature_dict()

    for card in cards:
        matrix[card.nature[0]][card.nature[1]] += 1

    return matrix


def natures_heatmap(matrix: nature_matrix, ts=datetime.now()):
    df = DataFrame(matrix)
    fig, ax = plt.subplots()
    hm = sns.heatmap(df, annot=True, ax=ax)

    hm.set_title(f'Nature Combinations Heatmap ({ts.strftime("%Y-%m-%d")})')

    return hm.get_figure()
