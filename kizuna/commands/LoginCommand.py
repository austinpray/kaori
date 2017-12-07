from kizuna.commands.Command import Command
from kizuna.utils import build_url
import config
from kizuna.models.User import User


class LoginCommand(Command):
    def __init__(self, make_session) -> None:
        help_text = "kizuna login - login to the web interface"
        self.make_session = make_session

        super().__init__('login', pattern='login', help_text=help_text, is_at=True)

    def respond(self, slack_client, message, matches):
        send = self.send_ephemeral_factory(slack_client, message['channel'], message['user'])
        session = self.make_session()
        user = User.get_by_slack_id(session, message['user'])

        if not user:
            return send("I don't have your users in the db. Prolly run 'kizuna refresh users' and if that still "
                        "doesn't fix it: Austin fucked up somewhere :^(")

        send(build_url(config.KIZUNA_WEB_URL, '/login', {'auth': user.get_token()}))
