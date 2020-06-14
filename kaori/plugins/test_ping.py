from unittest.mock import MagicMock

import pytest
from slackclient import SlackClient

from .ping import PingCommand
from ..adapters.slack import SlackAdapter, SlackMessage


@pytest.mark.asyncio
async def test_ping_cmd():
    sa = SlackAdapter(slack_client=SlackClient())

    sa._cached_bot_id = '@bogus'
    sa.reply = MagicMock()

    m1 = SlackMessage({
        'event': {
            'channel': 'XXX',
            'text': '@kaori ping',
        }
    })

    await PingCommand.handle(message=m1, bot=sa)

    sa.reply.assert_called_with(m1, 'pong')

    m2 = SlackMessage({
        'event': {
            'channel': 'XXX',
            'text': '@kaori bing',
        }
    })

    await PingCommand.handle(message=m2, bot=sa)

    sa.reply.assert_called_with(m2, 'BONG', create_thread=True)
