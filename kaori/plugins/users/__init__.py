import re

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter
from kaori.plugins.users.models.user import User
from kaori.skills.db import DB
from .models.user import User


class UserRefreshCommand(SlackCommand):
    """
    usage: {bot} refresh users - Make sure my users database is up-to-date with slack. You probably want to run this if
    someone has changed their name or a new user has joined slack.
    """

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB):
        if not bot.addressed_by(message):
            return

        match = bot.understands(message, with_pattern=re.compile('refresh users'))

        if not match:
            return

        res = bot.client.api_call('users.list')

        if not res['ok']:
            raise RuntimeError('call to users.list failed')

        slack_members = [member for member in res['members'] if not member['deleted']]

        with db.session_scope() as session:
            def maybe_create(slack_id):
                return User.maybe_create_user_from_slack_id(slack_id, bot.client, session)

            kaori_members = [maybe_create(member['id']) for member in slack_members]

            for member in kaori_members:
                el = [x for x in slack_members if x['id'] == member.slack_id]
                if not el:
                    continue

                el = el[0]

                if member.name != el['name']:
                    member.name = el['name']

        bot.reply(message, 'Refreshed users. :^)')


class UserNotFound(Exception):
    pass
