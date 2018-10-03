import json
import logging

import arrow
import falcon
from sqlalchemy import asc
from sqlalchemy.orm import sessionmaker

from kizuna.support.models import FaxMessage
from kizuna.support.utils import db_session_scope
from .utils import valid_auth_header


class FaxMessagesResource(object):
    def __init__(self, config, make_session: sessionmaker):
        self.config = config
        self.logger = logging.getLogger('kizuna_api.' + __name__)
        self.make_session = make_session

    def on_get(self, req, resp):
        if not valid_auth_header(self.config.API_KEY, req.auth):
            resp.status = falcon.HTTP_401
            return

        with db_session_scope(self.make_session) as session:
            messages = session \
                .query(FaxMessage) \
                .filter(FaxMessage.printed_at.is_(None)) \
                .order_by(asc(FaxMessage.created_at)) \
                .all()

            resp.body = json.dumps({'messages': [m.to_json_serializable() for m in messages]})


class FaxMessageResource(object):
    def __init__(self, config, make_session: sessionmaker):
        self.config = config
        self.make_session = make_session

    def on_put(self, req, resp, message_id):
        # todo: put me in a middleware
        if not valid_auth_header(self.config.API_KEY, req.auth):
            resp.status = falcon.HTTP_401
            return

        message_id = int(message_id)

        data = json.load(req.stream)

        with db_session_scope(self.make_session) as session:
            message = session.query(FaxMessage).filter(FaxMessage.id == message_id).first()

            if not message:
                resp.status = falcon.HTTP_404
                return

            if 'printed' not in data:
                resp.status = falcon.HTTP_400
                return

            printed = data['printed']
            message.printed_at = arrow.get().datetime if printed else None

            session.add(message)

        resp.body = json.dumps({'ok': True, 'msg': 'ayy lmao'})
