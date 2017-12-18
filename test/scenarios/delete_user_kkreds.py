from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
import arrow

from kizuna.models.User import User
from kizuna.models.KKredsTransaction import KKredsTransaction


if __name__ == "__main__":
    db_engine = create_engine(config.DATABASE_URL)
    make_session = sessionmaker(bind=db_engine)

    session = make_session()

    # should leave a kkred in the db
    ts = arrow.utcnow().timestamp
    from_user = User(name=f'bogus_from-{ts}',
                     slack_id=f'slack-from-{ts}',
                     api_key=f'from-{ts}')
    to_user = User(name=f'bogus_to-{ts}',
                   slack_id=f'slack-to-{ts}',
                   api_key=f'to-{ts}')

    session.add(from_user)
    session.add(to_user)

    trans = KKredsTransaction(from_user=from_user, to_user=to_user, amount=1000)

    session.add(trans)

    session.commit()

    session.delete(from_user)
    session.commit()
