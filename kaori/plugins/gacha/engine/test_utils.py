import pytest

from .utils import linear_scale, nt_sigmoid, make_sigmoid


def test_linear_scale():
    assert linear_scale(50, (1, 100), (1, 100)) == 50
    assert linear_scale(1, (1, 100), (1, 100)) == 1
    assert linear_scale(100, (1, 100), (1, 100)) == 100

    with pytest.raises(ValueError):
        linear_scale(0, (1, 100), (1, 100))

    assert linear_scale(100, (1, 100), (0, 1)) == 1
    assert linear_scale(1, (1, 100), (0, 1)) == 0
    assert linear_scale(50, (1, 100), (0, 1)) == 49 / 99

    assert linear_scale(11, (1, 11), (1, 100)) == 100


def test_sigmoid():
    assert nt_sigmoid(0, 1) == 1
    assert nt_sigmoid(-0.18, 0) == 0
    assert nt_sigmoid(-0.18, 0.5) == 0.59
    assert nt_sigmoid(-0.18, -0.5) == -0.59

    siggy = make_sigmoid(0.5)

    assert siggy(1) == 1
    assert siggy(0) == 0
    assert siggy(0.75) == 0.5
    assert siggy(-0.75) == -0.5
