from .lib import *

def test_humanize():

    assert humanize_nature(baby, clown) == 'baby clown'
    assert humanize_nature(clown, baby) == 'clown baby'
    assert humanize_nature(baby, cursed) == 'cursed baby'
    assert humanize_nature(cursed, baby) == 'cursed baby'
    assert humanize_nature(feral, cursed) == 'feral and cursed'
