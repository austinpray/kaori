from secrets import token_hex
from unittest.mock import MagicMock

import pytest
import ujson

from ....adapters.slack import SlackAdapter
from .battle import CardBattleCommand, _user_requesting_battle
from ..engine import RarityName
from ..models.Card import Card
from ..skills import CardBattler
from ...users import User
from ....skills import DB


@pytest.mark.asyncio
async def test_battle_cmd(fake_slack_msg_factory,
                          fake_slack_adapter: SlackAdapter,
                          test_db: DB):
    battler = CardBattler(player_url_base='https://battle.kaori.io/')

    with test_db.session_scope() as session:
        u = User(name=token_hex(5),
                 slack_id=token_hex(5),
                 api_key=token_hex(5))
        session.add(u)
        session.commit()
        user_id = u.id

        # TODO: desperately need a .make(...) method

        attacker = Card(owner=user_id,
                        creation_thread_ts=token_hex(5),
                        creation_thread_channel=token_hex(5),
                        published=True,
                        primary_nature='horny',
                        secondary_nature='feral',
                        creation_cursor='done')
        attacker_name = token_hex(5)
        attacker.set_name(attacker_name)
        attacker.set_rarity(RarityName.S)
        attacker.roll_stats()

        defender = Card(owner=user_id,
                        creation_thread_ts=token_hex(5),
                        creation_thread_channel=token_hex(5),
                        published=True,
                        primary_nature='baby',
                        secondary_nature='stupid',
                        creation_cursor='done')
        defender_name = token_hex(5)
        defender.set_name(defender_name)
        defender.set_rarity(RarityName.S)
        defender.roll_stats()

        session.add(attacker)
        session.add(defender)
        session.commit()

    message = fake_slack_msg_factory(text=f'@kaori battle {attacker_name} vs. {defender_name}')
    fake_slack_adapter.reply = MagicMock(return_value=None)

    assert fake_slack_adapter.addressed_by(message)

    match = _user_requesting_battle(message=message, bot=fake_slack_adapter)

    assert match is not None
    assert match[1] == attacker_name
    assert match[2] == defender_name

    await CardBattleCommand.handle(message=message,
                                   bot=fake_slack_adapter,
                                   battler=battler,
                                   db=test_db)

    fake_slack_adapter.reply.assert_called_once()

    # TODO (;;;*_*)
    kwargs = fake_slack_adapter.reply.call_args[1]
    assert kwargs is not None
    # TODO ╮(︶︿︶)╭
    reply = ujson.dumps(kwargs['blocks'])
    assert ujson.dumps('https://battle.kaori.io/?in=').strip('"') in reply
