from slacktools.chat import send, reply, send_factory, send_ephemeral, send_ephemeral_factory
from unittest.mock import MagicMock

class FakeClient:
    def api_call(self, *args, **kwargs):
        return args, kwargs

def test_send():
    """kinda useless tests but whatever"""
    slack_client = FakeClient()
    assert send(slack_client, 'general', 'ayy lmao')[1]['channel'] == 'general'
    assert send(slack_client, 'general', 'ayy lmao')[1]['text'] == 'ayy lmao'

    assert reply(slack_client, {'channel': 'general', 'user': 'UXXXYYYY'}, 'ayy lmao')[1]['channel'] == 'general'
    assert reply(slack_client, {'channel': 'general', 'user': 'UXXXYYYY'}, 'ayy lmao')[1]['text'] == '<@UXXXYYYY> ayy lmao'

    assert send_factory(slack_client, 'general')('ayy')[1]['channel'] == 'general'
    assert send_factory(slack_client, 'general')('ayy')[1]['text'] == 'ayy'

    assert send_ephemeral_factory(slack_client, 'general', 'UXXXYYYY')('ayy')[1]['user'] == 'UXXXYYYY'
