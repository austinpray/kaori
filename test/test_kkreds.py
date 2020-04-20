import arrow
from kaori.plugins.kkreds import is_payable, should_2020_04_mega_pay


def test_is_payable_time():
    # https://www.wolframalpha.com/input/?i=4am+central+to+UTC&dataset=
    samplegood1 = arrow.get('2013-01-11T10:20:58.970460+00:00')
    samplegood2 = arrow.get('2013-01-11T22:20:58.970460+00:00')
    samplegood3 = arrow.get('2013-05-11T09:20:58.970460+00:00')
    samplegood4 = arrow.get('2013-05-11T21:20:58.970460+00:00')
    good_2020_am = arrow.get('2020-04-20T09:20:58.970460+00:00')
    good_2020_pm = arrow.get('2020-04-20T21:20:58.970460+00:00')

    print(samplegood1.to('America/Chicago'))
    print(good_2020_am.to('America/Chicago'))
    print(good_2020_pm.to('America/Chicago'))

    assert is_payable(samplegood1) is True
    assert is_payable(samplegood2) is True
    assert is_payable(samplegood3) is True
    assert is_payable(samplegood4) is True
    assert is_payable(good_2020_am) is True
    assert is_payable(good_2020_pm) is True

    samplebad1 = arrow.get('2013-05-11T10:19:58.970460+00:00')
    samplebad2 = arrow.get('2013-05-11T10:21:58.970460+00:00')
    samplebad3 = arrow.get('2013-05-11T22:19:58.970460+00:00')
    samplebad4 = arrow.get('2013-05-11T22:19:58.970460+00:00')
    samplebad5 = arrow.get('2020-04-20T22:19:58.970460+00:00')
    assert is_payable(samplebad1) is False
    assert is_payable(samplebad2) is False
    assert is_payable(samplebad3) is False
    assert is_payable(samplebad4) is False
    assert is_payable(samplebad5) is False


def test_2020_mega_pay():
    good_2020_am = arrow.get('2020-04-20T09:20:58.970460+00:00')
    good_2020_pm = arrow.get('2020-04-20T21:20:58.970460+00:00')

    print(good_2020_am.to('America/Chicago'))
    print(good_2020_pm.to('America/Chicago'))

    assert should_2020_04_mega_pay(good_2020_am) is True
    assert should_2020_04_mega_pay(good_2020_pm) is True

    assert should_2020_04_mega_pay(arrow.get('2020-04-20T22:20:58.970460+00:00')) is False
    assert should_2020_04_mega_pay(arrow.get('2013-05-11T09:20:58.970460+00:00')) is False
