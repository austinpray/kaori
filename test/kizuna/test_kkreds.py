import arrow
from src.support.kkreds import is_payable


def test_is_payable_time():
    # https://www.wolframalpha.com/input/?i=4am+central+to+UTC&dataset=
    samplegood1 = arrow.get('2013-01-11T10:20:58.970460+00:00')
    samplegood2 = arrow.get('2013-01-11T22:20:58.970460+00:00')
    samplegood3 = arrow.get('2013-05-11T09:20:58.970460+00:00')
    samplegood4 = arrow.get('2013-05-11T21:20:58.970460+00:00')

    print(samplegood1.to('America/Chicago'))

    assert is_payable(samplegood1) is True
    assert is_payable(samplegood2) is True
    assert is_payable(samplegood3) is True
    assert is_payable(samplegood4) is True

    samplebad1 = arrow.get('2013-05-11T10:19:58.970460+00:00')
    samplebad2 = arrow.get('2013-05-11T10:21:58.970460+00:00')
    samplebad3 = arrow.get('2013-05-11T22:19:58.970460+00:00')
    samplebad4 = arrow.get('2013-05-11T22:19:58.970460+00:00')
    assert is_payable(samplebad1) is False
    assert is_payable(samplebad2) is False
    assert is_payable(samplebad3) is False
    assert is_payable(samplebad4) is False
