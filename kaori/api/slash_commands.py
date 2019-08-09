import logging

import falcon
from sqlalchemy.orm import sessionmaker

from kaori.support.models.FaxMessage import FaxMessage
from kaori.support.utils import db_session_scope


class SlashCommandsResource(object):

    def __init__(self, config, make_session: sessionmaker):
        self.config = config
        self.logger = logging.getLogger('kaori_api.' + __name__)
        self.make_session = make_session

    def on_post(self, req, resp):
        if not req.content_length:
            resp.status = falcon.HTTP_400
            resp.body = 'go away'
            return

        verification_token = req.get_param('token')
        if verification_token not in self.config.SLACK_WEBHOOK_TOKENS:
            resp.status = falcon.HTTP_401
            resp.body = 'this slack not allowed to send slash commands to kaori :/'
            return

        command = req.get_param('command')
        if command not in ['/faxaustin']:
            resp.status = falcon.HTTP_400
            resp.body = 'unknown command'
            return

        text = req.get_param('text')
        if not text:
            resp.status = falcon.HTTP_200
            resp.body = 'blank fax, you gotta type some text :^('
            return
        if len(text) > 280:
            resp.status = falcon.HTTP_200
            resp.body = 'faxes have to be 280 chars or less'
            return

        team_id = req.get_param('team_id', required=True)
        trigger_id = req.get_param('trigger_id', required=True)
        user_id = req.get_param('user_id', required=True)
        user_name = req.get_param('user_name', required=True)

        with db_session_scope(self.make_session) as session:
            message = FaxMessage(team_id=team_id,
                                 text=text,
                                 trigger_id=trigger_id,
                                 user_id=user_id,
                                 user_name=user_name)

            session.add(message)

        resp.body = 'sent fax to austin :^)'
