import arrow
import os
from uuid import uuid4

from . import is_payable, should_mega_pay, mega_pay_amount
from .models import KKredsTransaction
from ..users import User


def test_kkreds_balance():
    from . import get_kkred_balance
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from decimal import Decimal

    db_engine = create_engine(os.getenv('DATABASE_URL'))
    make_session = sessionmaker(bind=db_engine)

    session = make_session()

    # user should have a balance of 100 kkreds
    uniq = uuid4()
    from_user = User(name=f'bogus_from-{uniq}',
                     slack_id=f'slack-from-{uniq}',
                     api_key=f'from-{uniq}')
    to_user = User(name=f'bogus_to-{uniq}',
                   slack_id=f'slack-to-{uniq}',
                   api_key=f'to-{uniq}')

    session.add(from_user)
    session.add(to_user)

    trans1 = KKredsTransaction(to_user=from_user, amount=Decimal(1000))
    trans2 = KKredsTransaction(from_user=from_user, to_user=to_user, amount=Decimal('100.5'))

    session.add(trans1)
    session.add(trans2)

    session.commit()

    from_user_balance = get_kkred_balance(from_user, session)
    print(f'from_user balance {from_user_balance}')
    assert from_user_balance == Decimal('899.5')
    to_user_balance = get_kkred_balance(to_user, session)
    print(f'to_user balance {to_user_balance}')
    assert get_kkred_balance(to_user, session) == Decimal('100.5')

    third = User(name=f'bogus_third-{uniq}',
                 slack_id=f'slack-third-{uniq}',
                 api_key=f'third-{uniq}')

    session.add(third)

    trans3 = KKredsTransaction(to_user=third, amount=Decimal('0.0001'))

    session.add(trans3)

    session.commit()

    third_balance = get_kkred_balance(third, session)

    print(f'third balance {third_balance}')
    assert third_balance == Decimal('0.0001')

    # shouldn't be possible but should do it anyway
    trans4 = KKredsTransaction(from_user=third, amount=Decimal('100000'))

    session.add(trans4)

    session.commit()
    third_balance = get_kkred_balance(third, session)

    print(f'third balance {third_balance}')
    assert third_balance == Decimal('0.0001') - Decimal('100000')

    # session.delete(from_user)
    # session.delete(to_user)
    # session.delete(trans)
    # session.commit()


def test_kkreds_transaction():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    db_engine = create_engine(os.getenv('DATABASE_URL'))
    make_session = sessionmaker(bind=db_engine)

    session = make_session()

    # should leave a kkred in the db
    uniq = uuid4()
    from_user = User(name=f'bogus_from-{uniq}',
                     slack_id=f'slack-from-{uniq}',
                     api_key=f'from-{uniq}')
    to_user = User(name=f'bogus_to-{uniq}',
                   slack_id=f'slack-to-{uniq}',
                   api_key=f'to-{uniq}')

    session.add(from_user)
    session.add(to_user)

    trans = KKredsTransaction(from_user=from_user, to_user=to_user, amount=1000)

    session.add(trans)

    session.commit()

    session.delete(from_user)
    session.commit()


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


def test_2021_mega_pay():
    good_2021_am = arrow.get('2021-04-20T09:20:58.970460+00:00')
    good_2021_pm = arrow.get('2021-04-20T21:20:58.970460+00:00')

    print(good_2021_am.to('America/Chicago'))
    print(good_2021_pm.to('America/Chicago'))

    assert should_mega_pay(good_2021_am) is True
    assert should_mega_pay(good_2021_pm) is True

    assert should_mega_pay(arrow.get('2020-04-20T22:20:58.970460+00:00')) is False
    assert should_mega_pay(arrow.get('2013-05-11T09:20:58.970460+00:00')) is False

    assert mega_pay_amount(0, 0) == 4200
    assert mega_pay_amount(0, 1) == 4200
    assert mega_pay_amount(0, 500_000) == 3622
    assert mega_pay_amount(1, 0) == 3177
    assert mega_pay_amount(1, 100) == 3177
    assert mega_pay_amount(2, 0) == 2538
    assert mega_pay_amount(30, 0) == 210
    assert mega_pay_amount(59, 0) == 4
    assert mega_pay_amount(60, 0) == 0
