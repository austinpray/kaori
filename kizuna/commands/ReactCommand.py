from .Command import Command

from config import KIZUNA_WEB_URL
from kizuna.models.User import User
from kizuna.utils import build_url


class ReactCommand(Command):
    def __init__(self, Session) -> None:
        help_text = 'kizuna react - view available reaction images and tags\n' \
                    'kizuna react add - upload some reaction images\n' \
                    'kizuna react <tag> - Send a reaction related to the tag'
        self.Session = Session
        super().__init__(name='react',
                         pattern='react(?:ion)?(?: (.*))?$',
                         help_text=help_text,
                         is_at=True)

    def respond(self, slack_client, message, matches):
        send = self.send_ephemeral_factory(slack_client, message['channel'], message['user'])

        session = self.Session()
        user = User.get_by_slack_id(session, message['user'])

        if not user:
            return send("I don't have your users in the db. Prolly run 'kizuna refresh users' and if that still "
                        "doesn't fix it: Austin fucked up somewhere :^(")

        def authenticated_path(path):
            return build_url(KIZUNA_WEB_URL, path, {'auth': user.get_token()})

        if not matches[0]:
            # kizuna react$
            url = authenticated_path('/react')
            return send(url)

        if matches[0] == 'add':
            # kizuna react add
            return send(authenticated_path('/react/images/new'))

        # kizuna react <tag>
        return send("I'm not ready for `kizuna react <tag>` yet :(")
