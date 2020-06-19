from secrets import token_hex
from time import time
from unittest.mock import Mock, MagicMock

from slackclient import SlackClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import kaori.plugins.gacha as gacha_plugin
from kaori import test_config
from kaori.adapters.slack import SlackAdapter
from kaori.plugins.gacha.models.Card import Card
from kaori.plugins.users import User
from kaori.skills import DB, LocalFileUploader
from kaori.support import Kaori


def test_card_creation_state_happy():
    config = test_config
    db_engine = create_engine(config.DATABASE_URL)
    make_session = sessionmaker(bind=db_engine, autoflush=False)

    k = Kaori()

    initial_ts = str(time())
    slack = Mock(spec=SlackClient)
    slack.api_call = MagicMock(return_value={
        'ok': True,
        'ts': initial_ts,
    })
    adapter = SlackAdapter(slack_client=slack)
    adapter._cached_bot_id = token_hex(2)
    k.adapters['slack'] = adapter

    db = DB(make_session=make_session)

    k.skills |= {
        db,
    }

    k.skills.add(LocalFileUploader())

    k.plugins |= {
        gacha_plugin,
    }

    slack_id = token_hex(5)

    session: Session
    with db.session_scope() as session:
        u = User(name='Ridwan',
                 slack_id=slack_id,
                 api_key=token_hex(5))
        session.add(u)
        session.commit()
        user_id = u.id

    def handle(msg):
        k.handle('slack', msg)

    channel = "CXXXXXX"

    def user_message(**kwargs):
        ts = time()
        return {
            "team_id": "TXXXX",
            "event": {
                "type": "message",
                "user": slack_id,
                "ts": ts,
                "channel": channel,
                "event_ts": ts,
                "channel_type": "channel",
                **kwargs,
            },
            "type": "event_callback",
        }

    with db.session_scope() as session:
        handle(user_message(text='@kaori create card', ts=initial_ts, event_ts=initial_ts))

        card = session.query(Card) \
            .join(User) \
            .filter(Card.creation_thread_ts == initial_ts) \
            .first()

        assert card.owner == user_id
        assert card.creation_cursor == 'set_name'

        name = f'Matt Morgan {token_hex(2)}'

        handle(user_message(text=f'@kaori {name}', thread_ts=initial_ts))

        session.refresh(card)
        assert card.name == name
        assert card.creation_cursor == 'set_image'

        # TODO skipping over image uploading lmao
        card.creation_cursor = 'set_description'
        session.commit()

        handle(user_message(text=f'@kaori ubu uwu', thread_ts=initial_ts))

        session.refresh(card)
        assert card.description == 'ubu uwu'

        handle(user_message(text=f'@kaori stupid feral', thread_ts=initial_ts))

        session.refresh(card)
        assert card.primary_nature == 'stupid'
        assert card.secondary_nature == 'feral'

        handle(user_message(text=f'@kaori S', thread_ts=initial_ts))

        session.refresh(card)
        assert card.rarity_string() == 'S'

        assert card.published is False

        handle(user_message(text=f'@kaori yes', thread_ts=initial_ts))

        session.refresh(card)
        assert card.published is True
        assert card.creation_cursor == 'done'
