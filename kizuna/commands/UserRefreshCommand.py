from kizuna.commands.Command import Command

from kizuna.models.User import User


class UserRefreshCommand(Command):
    def __init__(self, db_session) -> None:

        self.db_session = db_session

        help_text = "kizuna refresh users - Make sure my users database is up-to-date with slack. You probably want " \
                    "to run this if someone has changed their name or a new user has joined slack."
        super().__init__(name="refresh-user",
                         pattern='refresh users$',
                         help_text=help_text,
                         is_at=True)

    def respond(self, slack_client, message, matches):
        session = self.db_session()

        res = slack_client.api_call('users.list')

        if not res['ok']:
            raise RuntimeError('call to users.list failed')

        slack_members = [member for member in res['members'] if not member['deleted']]

        def maybe_create(slack_id):
            return User.maybe_create_user_from_slack_id(slack_id, slack_client, session)

        kizuna_members = [maybe_create(member['id']) for member in slack_members]

        for member in kizuna_members:
            el = [x for x in slack_members if x['id'] == member.slack_id]
            if not el:
                continue

            el = el[0]

            if member.name != el['name']:
                member.name = el['name']

        session.commit()
        self.send(slack_client, message['channel'], 'Refreshed users. :^)')
