from uuid import uuid4

import pytest
from sqlalchemy.orm import Session

from kaori.plugins.gacha.engine import RarityName
from .Card import Card, get_game_cards


def test_sluggify():
    assert Card.sluggify_name('') == ''
    assert Card.sluggify_name('Austin Pray') == 'austin-pray'

    a100 = 'a' * 100
    assert Card.sluggify_name(a100) == a100
    assert Card.sluggify_name(a100.upper()) == a100

    r = 'Rhoshandiatellyneshiaunneveshenk ' * 100
    r_exp = '-'.join(['rhoshandiatellyneshiaunneveshenk'] * 100)

    assert Card.sluggify_name(r) == r_exp

    assert Card.sluggify_name('👩🏿‍🍳') == 'xn--qj8hxirk'

    # note that this test case is basically undefined behavior
    # assert Card.sluggify_name('👩🏿‍🍳'*50) == ''

    assert Card.sluggify_name('Iñtërnâtiônàlizætiøn☃💪') == 'xn--itrntinliztin-vdb0a5exd8ewcyey495hncp2g'


def test_get_game_cards(make_fake_user, db_session: Session):
    uniq1 = str(uuid4())
    uniq2 = str(uuid4())
    name_a = f'a-{__name__}'
    name_b = f'b-{__name__}'

    db_session.query(Card).filter(Card.name.in_((name_a, name_b))).delete(synchronize_session=False)

    db_session.commit()

    fake_user = make_fake_user()

    db_session.add(fake_user)

    card_a = Card(name=uniq2,
                  slug=uniq2,
                  owner=fake_user.id,
                  published=True,
                  primary_nature='stupid',
                  secondary_nature='clown',
                  creation_thread_channel=f'ch-{uniq2}',
                  creation_thread_ts=f'ts-{uniq2}')

    card_b = Card(name=uniq1,
                  slug=uniq1,
                  owner=fake_user.id,
                  published=True,
                  primary_nature='stupid',
                  secondary_nature='baby',
                  creation_thread_channel=f'ch-{uniq1}',
                  creation_thread_ts=f'ts-{uniq1}')

    card_a.set_rarity(RarityName.S)
    card_b.set_rarity(RarityName.S)

    db_session.add(card_a)
    db_session.add(card_b)
    db_session.commit()

    game_cards = get_game_cards(db_session)

    assert game_cards

    assert uniq1 in [gc.name for gc in game_cards]
    assert uniq2 in [gc.name for gc in game_cards]

    game_cards = get_game_cards(db_session, user=fake_user.id)

    assert game_cards
    assert len(game_cards) == 2

    assert uniq1 in [gc.name for gc in game_cards]
    assert uniq2 in [gc.name for gc in game_cards]

    game_cards = get_game_cards(db_session, user=fake_user)

    assert game_cards
    assert len(game_cards) == 2

    assert uniq1 in [gc.name for gc in game_cards]
    assert uniq2 in [gc.name for gc in game_cards]

    game_cards = get_game_cards(db_session, user_slack_id=fake_user.slack_id)

    assert game_cards
    assert len(game_cards) == 2

    assert uniq1 in [gc.name for gc in game_cards]
    assert uniq2 in [gc.name for gc in game_cards]

    game_cards = get_game_cards(db_session, user_slack_id=str(uuid4()))

    assert not game_cards

    with pytest.raises(ValueError):
        get_game_cards(db_session, user=str(uuid4()))
