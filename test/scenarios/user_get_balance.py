from kizuna.models.User import User
from kizuna.models.KKredsTransaction import KKredsTransaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import arrow
import config
from decimal import Decimal


if __name__ == "__main__":
    db_engine = create_engine(config.DATABASE_URL)
    make_session = sessionmaker(bind=db_engine)

    session = make_session()

    # user should have a balance of 100 kkreds
    ts = arrow.utcnow().timestamp
    from_user = User(name=f'bogus_from-{ts}',
                     slack_id=f'slack-from-{ts}',
                     api_key=f'from-{ts}')
    to_user = User(name=f'bogus_to-{ts}',
                   slack_id=f'slack-to-{ts}',
                   api_key=f'to-{ts}')

    session.add(from_user)
    session.add(to_user)

    trans1 = KKredsTransaction(to_user=from_user, amount=Decimal(1000))
    trans2 = KKredsTransaction(from_user=from_user, to_user=to_user, amount=Decimal('100.5'))

    session.add(trans1)
    session.add(trans2)

    session.commit()

    from_user_balance = from_user.get_kkred_balance(session)
    print(f'from_user balance {from_user_balance}')
    assert from_user_balance == Decimal('899.5')
    to_user_balance = to_user.get_kkred_balance(session)
    print(f'to_user balance {to_user_balance}')
    assert to_user.get_kkred_balance(session) == Decimal('100.5')

    third = User(name=f'bogus_third-{ts}',
                 slack_id=f'slack-third-{ts}',
                 api_key=f'third-{ts}')

    session.add(third)

    trans3 = KKredsTransaction(to_user=third, amount=Decimal('0.0001'))

    session.add(trans3)

    session.commit()

    third_balance = third.get_kkred_balance(session)

    print(f'third balance {third_balance}')
    assert third_balance == Decimal('0.0001')

    # shouldn't be possible but should do it anyway
    trans4 = KKredsTransaction(from_user=third, amount=Decimal('100000'))

    session.add(trans4)

    session.commit()
    third_balance = third.get_kkred_balance(session)

    print(f'third balance {third_balance}')
    assert third_balance == Decimal('0.0001') - Decimal('100000')


    # session.delete(from_user)
    # session.delete(to_user)
    # session.delete(trans)
    # session.commit()

