from kizuna.support import Kizuna
from kizuna.adapters import Adapter
from kizuna.adapters.slack import SlackAdapter
import kizuna.plugins.ping

class FakeSlackClient:
    def api_call(*args, **kwargs):
        if args[0] == 'auth.test':
            return {'user_id': 'UKIZUNAAA'}

        print(kwargs.get('text'), end='')

slack_ping_message = {
    "token": "BOGUS",
    "team_id": "BOGUS_TEAM",
    "api_app_id": "BOGUS_APP_ID",
    "event": {
        "type": "message",
        "user": "UUSERRRRR",
        "text": "<@UKIZUNAAA> ping",
        "client_msg_id": "fda9651b-3467-4a98-861b-3b254c1614c6",
        "ts": "1538496960.000100",
        "channel": "C5H8YMX3Q",
        "event_ts": "1538496960.000100",
        "channel_type": "channel"
    },
    "type": "event_callback",
    "event_id": "EvD5NLL82H",
    "event_time": 1538496960,
    "authed_users": [
        "UUUUUUUU1",
        "UUUUUUUU2"
    ]
}

def test_plugin(capsys):
    k = Kizuna()
    k.adapters['slack'] = SlackAdapter(slack_client=FakeSlackClient)
    k.plugins |= {kizuna.plugins.ping}
    k.handle('slack', slack_ping_message.copy())
    out, err = capsys.readouterr()
    assert out == '<@UUSERRRRR> pong'
