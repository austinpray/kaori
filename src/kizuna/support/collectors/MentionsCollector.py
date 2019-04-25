from slacktools.message import extract_mentions

from . import BaseCollector
from ..models import User, AtGraphEdge
from ..utils import db_session_scope


class MentionsCollector(BaseCollector):

    def __init__(self, db_session_maker, slack_client=None) -> None:
        self.slack_client = slack_client
        self.db_session_maker = db_session_maker

    def collect(self, message):
        mentioned_user_ids = extract_mentions(message['text'])

        if not mentioned_user_ids or len(mentioned_user_ids) < 1:
            return

        with db_session_scope(self.db_session_maker) as session:
            try:
                def id_to_user(mentioned_user_id):
                    return User.maybe_create_user_from_slack_id(mentioned_user_id, self.sc, session)

                from_user = id_to_user(message['user'])
                mentioned_users = list(map(id_to_user, mentioned_user_ids))
            except ValueError as err:
                print('Error: probably had trouble finding user by id')
                print(err)
                return

            for mentioned_user in mentioned_users:
                AtGraphEdge.increment_edge(from_user, mentioned_user, session)
