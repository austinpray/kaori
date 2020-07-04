import os
from pathlib import Path
from secrets import token_hex
from time import time
from unittest.mock import Mock, MagicMock
from uuid import uuid4

import pytest
from slackclient import SlackClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from kaori.plugins.kkreds import KKredsTransaction
from kaori.plugins.users import User
from .adapters.slack import SlackMessage, SlackAdapter
from .skills import DB


@pytest.fixture
def db_session() -> Session:
    make_session = db_sessionmaker()
    session = make_session()
    return session


def db_sessionmaker():
    db_engine = create_engine(os.getenv('DATABASE_URL'))
    make_session = sessionmaker(bind=db_engine)
    return make_session


@pytest.fixture
def test_db() -> DB:
    return DB(make_session=db_sessionmaker())


@pytest.fixture
def fake_slack_msg_factory() -> callable:
    from uuid import uuid4

    def __make_msg(**kwargs):
        ts = time()
        return SlackMessage({
            "team_id": "TXXXX",
            "event": {
                "type": "message",
                "user": str(uuid4()),
                "ts": ts,
                "channel": f'channel-{str(uuid4())}',
                "event_ts": ts,
                "channel_type": "channel",
                **kwargs,
            },
            "type": "event_callback",
        })

    return __make_msg


@pytest.fixture()
def fake_slack_adapter() -> SlackAdapter:
    slack = Mock(spec=SlackClient)
    # TODO: smelly, why do we have to mock this?
    slack.api_call = MagicMock(return_value={
        'ok': True,
        'ts': str(time()),
    })
    adapter = SlackAdapter(slack_client=slack)
    # TODO: smelly, why are we modifying protected stuff in tests?
    adapter._cached_bot_id = token_hex(2)

    return adapter


@pytest.fixture()
def fake_user(test_db: DB) -> User:
    with test_db.session_scope() as session:
        name = str(uuid4())

        u = User(name=f'{name}-user',
                 slack_id=f'{name}-slack-id',
                 api_key=str(uuid4()))

        session.add(u)
        session.commit()

        return u


@pytest.fixture()
def make_fake_user(test_db: DB) -> callable:
    def make_user():
        session: Session
        with test_db.session_scope() as session:
            name = str(uuid4())

            u = User(name=f'{name}-user',
                     slack_id=f'{name}-slack-id',
                     api_key=str(uuid4()))

            session.add(u)
            session.commit()
            session.refresh(u)
            session.expunge(u)

            return u

    return make_user


@pytest.fixture()
def grant_kkreds(test_db: DB) -> callable:
    def fn(user: User, kkreds: int):
        session: Session
        with test_db.session_scope() as session:
            session.add(KKredsTransaction(to_user=user, amount=kkreds))
            session.commit()

    return fn


_project_root = Path(__file__).parent.parent


@pytest.fixture()
def project_root() -> Path:
    return _project_root


@pytest.fixture()
def project_tmp() -> Path:
    tmp = _project_root.joinpath('static/tmp')
    tmp.mkdir(parents=True, exist_ok=True)
    return tmp


@pytest.fixture()
def find_nested_text():
    def _fn(d) -> str:
        text = []

        if type(d) == list:
            d = enumerate(d)

        if type(d) == dict:
            d = d.items()

        for k, v in d:
            if k == 'text' and type(v) == str:
                text.append(v)

            if type(v) == dict:
                text.append(_fn(v))

        return "\n".join(text)

    return _fn
