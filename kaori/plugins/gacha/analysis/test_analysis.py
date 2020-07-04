from pandas import DataFrame

from kaori.plugins.gacha.engine import NatureName, RarityName
from kaori.plugins.gacha.engine.core import Card as GameCard

from .natures import get_nature_matrix, natures_heatmap
from pathlib import Path
from uuid import uuid4

from .rarity import get_rarity_dist, rarity_histogram


def test_analysis(project_tmp: Path):
    from ..engine.test.cards import sachiko, matt_morgan, ubu, xss, balanced_S, low_dmg

    data = [sachiko, matt_morgan, ubu, ubu, xss, balanced_S, low_dmg]

    matrix = get_nature_matrix(data)

    assert matrix[('cursed', 'feral')] == 2

    hm = natures_heatmap(matrix)

    hm.savefig(str(project_tmp.joinpath('test-natures-breakdown.png')))

    rdist = get_rarity_dist(data)

    assert rdist[RarityName.S] == 4
    assert rdist[RarityName.A] == 0

    hist = rarity_histogram(rdist)

    hist.savefig(str(project_tmp.joinpath('test-rarity-breakdown.png')))

    nature_matrix = get_nature_matrix([
        GameCard(name=str(uuid4()), rarity=RarityName.S, nature=(NatureName.cursed, NatureName.clown)),
        GameCard(name=str(uuid4()), rarity=RarityName.S, nature=(NatureName.clown, NatureName.cursed)),
        GameCard(name=str(uuid4()), rarity=RarityName.S, nature=(NatureName.stupid, NatureName.clown)),
    ])

    hm = natures_heatmap(nature_matrix)

    hm.savefig(str(project_tmp.joinpath('test-reduced-natures-breakdown.png')))
