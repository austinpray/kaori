from unittest.mock import MagicMock

import pytest
from slackclient import SlackClient

from .clap import ClapCommand
from ..adapters.slack import SlackAdapter, SlackMessage


@pytest.mark.asyncio
async def test_clap_cmd():
    sa = SlackAdapter(slack_client=SlackClient())

    sa._cached_bot_id = '@bogus'
    sa.respond = MagicMock()

    msg = SlackMessage({
        'event': {
            'channel': 'XXX',
            'text': '@kaori clap ayy lmao',
        }
    })

    await ClapCommand.handle(message=msg, bot=sa)
