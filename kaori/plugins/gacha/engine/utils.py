import sys
from functools import partial
from typing import Tuple, Union

Number = Union[int, float]


def sign(x: Number) -> Number:
    return bool(x > 0) - bool(x < 0)


def linear_scale(x: Number,
                 x_range: Tuple[Number, Number],
                 target_range: Tuple[Number, Number]) -> Number:
    """
    https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)
    """

    x_min = min(x_range)
    x_max = max(x_range)

    if not x_min <= x <= x_max:
        raise ValueError(f'{x} is not between {x_min} and {x_max}')

    a = min(target_range)
    b = max(target_range)
    return a + (x - x_min) * (b - a) / (x_max - x_min)


def nt_sigmoid(k: Number, x: Number) -> Number:
    """
    Normalized Tunable Sigmoid Function

    k tunes the sigmoid curve, should be between -1 and 1
    x is the input
    outputs ranges from 0 to 1

    https://dhemery.github.io/DHE-Modules/technical/sigmoid/
    https://dinodini.wordpress.com/2010/04/05/normalized-tunable-sigmoid-functions/
    """
    return (x - k * x) / (k - 2 * k * abs(x) + 1)


def make_sigmoid(k: Number) -> callable:
    return partial(nt_sigmoid, k)


def trim_doc(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = float('inf')
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < float('inf'):
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)
