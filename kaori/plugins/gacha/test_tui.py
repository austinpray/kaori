import re

from .engine import NatureName
from .tui import get_nature_examples, card_stats_blocks


def test_nature_examples():
    assert len(get_nature_examples()) == 2
    match = re.match(f'`@kaori ({NatureName.to_regex()}) ({NatureName.to_regex()})`', get_nature_examples()[0], re.I)
    assert match is not None


def test_stats_blocks(find_nested_text):
    assert 'total of 1 card ' in find_nested_text(card_stats_blocks(card_total=1))
    assert 'total of 2 cards ' in find_nested_text(card_stats_blocks(card_total=2))
