import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture
def db_session() -> Session:
    db_engine = create_engine(os.getenv('DATABASE_URL'))
    make_session = sessionmaker(bind=db_engine)
    session = make_session()
    return session
