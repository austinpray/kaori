from unittest.mock import MagicMock

import pytest
import ujson
from kaori.adapters.slack import SlackAdapter

from .support import CardHelpCommand, CardPriceCommand


@pytest.mark.asyncio
async def test_battle_cmd(fake_slack_msg_factory,
                          fake_slack_adapter: SlackAdapter):

    bogus_message = fake_slack_msg_factory(text=f'@kaori asldfkjslkdjf')
    fake_slack_adapter.reply = MagicMock(return_value={'ok': True})

    await CardHelpCommand.handle(bogus_message, bot=fake_slack_adapter)
    await CardPriceCommand.handle(bogus_message, bot=fake_slack_adapter)

    fake_slack_adapter.reply.assert_not_called()

    await CardHelpCommand.handle(
        fake_slack_msg_factory(
            text='@kaori cards help',
            bot=fake_slack_adapter,
        ),
        bot=fake_slack_adapter
    )

    ehhhh = ujson.dumps(fake_slack_adapter.reply.call_args[1])
    assert 'kaori show cards' in ehhhh
    assert 'kaori battle NAME vs. NAME' in ehhhh

    await CardPriceCommand.handle(
        fake_slack_msg_factory(
            text='@kaori card prices',
            bot=fake_slack_adapter,
        ),
        bot=fake_slack_adapter
    )

    ehhhh = ujson.dumps(fake_slack_adapter.reply.call_args[1])
    assert 'price breakdown by rank' in ehhhh
