from kizuna.AtGraph import extract_ats
from kizuna.AtGraphEdge import AtGraphEdge
from kizuna.Command import Command

from kizuna.User import User


class AtGraphDataCollector(Command):
    def __init__(self, db_session, slack_client) -> None:
        super().__init__('at-graph-data-collector', '.*', '', False)
        self.db_session = db_session
        self.sc = slack_client

    def maybe_respond(self, slack_client, message):
        mentioned_user_ids = extract_ats(message['text'])

        if not mentioned_user_ids or len(mentioned_user_ids) < 1:
            return

        session = self.db_session()

        # make sure all users exist in db before we do graph operations
        try:
            def id_to_user(mentioned_user_id):
                return User.maybe_create_user_from_slack_id(mentioned_user_id, self.sc, session)

            from_user = id_to_user(message['user'])
            mentioned_users = list(map(id_to_user, mentioned_user_ids))
        except ValueError as err:
            print('Error: probably had trouble finding user by id')
            print(err)
            return

        #session.commit()

        for mentioned_user in mentioned_users:
            AtGraphEdge.increment_edge(from_user, mentioned_user, session)

        session.commit()


