from .Command import Command

from config import KIZUNA_WEB_URL
from urllib.parse import urljoin


class ReactCommand(Command):
    def __init__(self) -> None:
        help_text = 'kizuna react - view available reaction images and tags\n'\
                    'kizuna react <tag> - Send a reaction related to the tag'
        super().__init__(name='react',
                         pattern='react(?:ion)?(?: (.*))?$',
                         help_text=help_text,
                         is_at=True)

    def respond(self, slack_client, message, matches):
        send = self.send_ephemeral_factory(slack_client, message['channel'], message['user'])

        if not matches[0]:
            # kizuna react$
            return send(urljoin(KIZUNA_WEB_URL, '/react'))

        if matches[0] == 'add':
            # kizuna react add
            return send(urljoin(KIZUNA_WEB_URL, '/react/images/new'))

        # kizuna react <tag>
        return send("I'm not ready for `kizuna react <tag>` yet :(")
