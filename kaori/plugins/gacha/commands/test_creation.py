from secrets import token_hex
from time import time
from unittest.mock import Mock, MagicMock
from uuid import uuid4

from slackclient import SlackClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import kaori.plugins.gacha as gacha_plugin
from kaori import test_config
from kaori.adapters.slack import SlackAdapter
from kaori.plugins.gacha.engine import RarityName
from kaori.plugins.gacha.models.Card import Card
from kaori.plugins.users import User
from kaori.skills import DB, LocalFileUploader
from kaori.support import Kaori
from .creation import user_extract_rarity, charge_for_card
from ..skills import CardBattler


def test_rarity_extract():
    assert user_extract_rarity('yeah this is bogus') is None
    assert user_extract_rarity("Yeah i'm thinkin S-tier card") is RarityName.S
    assert user_extract_rarity("Yeah i'm thinkin B card") is RarityName.B
    assert user_extract_rarity("B") is RarityName.B
    assert user_extract_rarity("b") is RarityName.B
    assert user_extract_rarity("    B     ") is RarityName.B

    # tricky
    #                          "this should be AN F card" is correct english afaik.
    #                          Gonna let the dummies slide regardless
    assert user_extract_rarity("this should be a F card") is RarityName.F
    assert user_extract_rarity("I'm thinking a S-tier card") is RarityName.S


def test_card_creation_state_happy(make_fake_user, grant_kkreds):
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
        CardBattler(player_url_base='https://battle.kaori.io/')
    }

    k.skills.add(LocalFileUploader())

    k.plugins |= {
        gacha_plugin,
    }

    u: User = make_fake_user()
    slack_id = u.slack_id
    user_id = u.id

    grant_kkreds(u, 1e10)

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


def test_charge_for_card(make_fake_user, grant_kkreds, db_session: Session):
    kaori = make_fake_user()
    fake_user = make_fake_user()
    db_session.add(kaori)
    db_session.add(fake_user)
    uniq2 = str(uuid4())
    card_a = Card(name=uniq2,
                  slug=uniq2,
                  owner=fake_user.id,
                  published=False,
                  rarity=500,
                  primary_nature='stupid',
                  secondary_nature='clown',
                  creation_thread_channel=f'ch-{uniq2}',
                  creation_thread_ts=f'ts-{uniq2}')

    db_session.add(card_a)
    db_session.commit()

    success, reason = charge_for_card(card=card_a, session=db_session, kaori_user=kaori)

    assert success is False
    assert 'do not have enough kkreds' in reason

    db_session.expunge(fake_user)
    grant_kkreds(fake_user, 1e10)
    db_session.add(fake_user)

    success, reason = charge_for_card(card=card_a, session=db_session, kaori_user=kaori)

    assert 'paid for card' in reason
    assert success is True
