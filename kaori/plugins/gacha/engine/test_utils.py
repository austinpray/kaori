from decimal import Decimal

import pytest

from .utils import linear_scale


def test_linear_scale():
    assert linear_scale(50, (1, 100), (1, 100)) == 50
    assert linear_scale(1, (1, 100), (1, 100)) == 1
    assert linear_scale(100, (1, 100), (1, 100)) == 100

    with pytest.raises(ValueError):
        linear_scale(0, (1, 100), (1, 100))

    assert linear_scale(100, (1, 100), (0, 1)) == 1
    assert linear_scale(1, (1, 100), (0, 1)) == 0
    assert linear_scale(50, (1, 100), (0, 1)) == 49/99

    assert linear_scale(11, (1, 11), (1, 100)) == 100

