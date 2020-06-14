from .core import RarityName, NatureName
import re

def test_enum_regexes():
    assert re.search(f'({RarityName.to_regex()})', 'please make it S-tier')[1] == 'S'
    nature_re = NatureName.to_regex()
    match = re.search(f'({nature_re}).*({nature_re})', 'hullo plz horny and clown, thx u')
    assert match[1] == 'horny'
    assert match[2] == 'clown'
