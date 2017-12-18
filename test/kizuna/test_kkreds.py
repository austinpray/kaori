import arrow
from kizuna.kkreds import is_payable


def test_is_payable_time():
    # https://www.wolframalpha.com/input/?i=4am+central+to+UTC&dataset=
    samplegood1 = arrow.utcnow().replace(hour=10, minute=20)
    samplegood2 = arrow.utcnow().replace(hour=22, minute=20)

    assert is_payable(samplegood1) is True
    assert is_payable(samplegood2) is True

    samplebad1 = arrow.utcnow().replace(hour=10, minute=10)
    samplebad2 = arrow.utcnow().replace(hour=1, minute=30)
    assert is_payable(samplebad1) is False
    assert is_payable(samplebad2) is False
