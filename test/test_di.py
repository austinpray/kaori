from abc import ABC

from kaori.support.di import build_di_args


# abc zone

class _Vehicle(ABC):
    pass


class _Car(_Vehicle):
    pass


# reggo classes

class _Cute:
    pass


class _CatGirl(_Cute):
    pass


def _handle_car(car: _Car):
    pass


def _handle_vehicle(car: _Vehicle):
    pass


def _handle_cute(cute: _Cute):
    pass


def _handle_cat_girl(owo: _CatGirl):
    pass


def test_di():
    car = _Car()
    cat_girl = _CatGirl()
    components = {car, cat_girl}
    explicit = build_di_args(components, _handle_car)
    assert car in explicit.values()
    implied = build_di_args(components, _handle_vehicle)
    assert car in implied.values()

    explicit = build_di_args(components, _handle_cat_girl)
    assert cat_girl in explicit.values()
    implied = build_di_args(components, _handle_cute)
    assert cat_girl in implied.values()
