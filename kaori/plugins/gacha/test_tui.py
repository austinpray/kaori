import re

from .engine import NatureName
from .tui import get_nature_examples


def test_nature_examples():
    assert len(get_nature_examples()) == 2
    match = re.match(f'`@kaori ({NatureName.to_regex()}) ({NatureName.to_regex()})`', get_nature_examples()[0], re.I)
    assert match is not None
