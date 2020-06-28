from .Card import Card


def test_sluggify():
    assert Card.sluggify_name('') == ''
    assert Card.sluggify_name('Austin Pray') == 'austin-pray'

    a100 = 'a'*100
    assert Card.sluggify_name(a100) == a100
    assert Card.sluggify_name(a100.upper()) == a100

    r = 'Rhoshandiatellyneshiaunneveshenk '*100
    r_exp = '-'.join(['rhoshandiatellyneshiaunneveshenk']*100)

    assert Card.sluggify_name(r) == r_exp

    assert Card.sluggify_name('👩🏿‍🍳') == 'xn--qj8hxirk'

    # note that this test case is basically undefined behavior
    # assert Card.sluggify_name('👩🏿‍🍳'*50) == ''

    assert Card.sluggify_name('Iñtërnâtiônàlizætiøn☃💪') == 'xn--itrntinliztin-vdb0a5exd8ewcyey495hncp2g'

