import json
import logging

import arrow
import falcon
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.message import Message
from falcon import Request
from slacktools.authorization import verify_signature
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

import config
from src.support.models.FaxMessage import FaxMessage
from src.support.utils import db_session_scope

db_engine = create_engine(config.DATABASE_URL)
make_session = sessionmaker(bind=db_engine)

rabbitmq_broker = RabbitmqBroker(url=config.RABBITMQ_URL)


class HealthCheckResource(object):
    def on_get(self, req, resp):
        resp.body = '{"ok": true}'


class EventsResource(object):

    def __init__(self):
        self.logger = logging.getLogger('kizuna_api.' + __name__)

    def on_post(self, req: Request, resp):

        go_away = json.dumps({'ok': False, 'msg': 'go away'})

        if not req.content_length:
            resp.status = falcon.HTTP_400
            resp.body = go_away
            return

        # defaults to utf8 but should probably look at http headers to get this value, charset and stuff
        body = req.bounded_stream.read().decode('utf8')

        try:
            if not verify_signature(config.SLACK_SIGNING_SECRET,
                                    int(req.get_header('X-Slack-Request-Timestamp')),
                                    body,
                                    req.get_header('X-Slack-Signature')):
                resp.status = falcon.HTTP_401
                resp.body = go_away
                return
        except ValueError as e:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'ok': False, 'msg': str(e)})
            return

        doc = json.loads(body)
        callback_type = doc['type']

        if callback_type == 'url_verification':
            resp.body = doc['challenge']
            return

        if callback_type == 'event_callback':
            event = doc['event']
            event_type = event['type']
            if event_type == 'message':
                self.logger.debug(event)
                rabbitmq_broker.enqueue(Message(queue_name='default',
                                                actor_name='worker',
                                                args=(event,),
                                                options={},
                                                kwargs={}))

        resp.body = json.dumps({'ok': True, 'msg': 'thanks!'})


class SlashCommandsResource(object):

    def __init__(self):
        self.logger = logging.getLogger('kizuna_api.' + __name__)

    def on_post(self, req, resp):
        if not req.content_length:
            resp.status = falcon.HTTP_400
            resp.body = 'go away'
            return

        verification_token = req.get_param('token')
        if verification_token not in config.SLACK_WEBHOOK_TOKENS:
            resp.status = falcon.HTTP_401
            resp.body = 'this slack not allowed to send slash commands to kizuna :/'
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

        with db_session_scope(make_session) as session:
            message = FaxMessage(team_id=team_id,
                                 text=text,
                                 trigger_id=trigger_id,
                                 user_id=user_id,
                                 user_name=user_name)

            session.add(message)

        resp.body = 'sent fax to austin :^)'


def valid_auth_header(auth_header) -> bool:
    if not auth_header:
        return False

    auth_token = auth_header.split(' ')[1]

    if not auth_token or auth_token != config.API_KEY:
        return False

    return True


class FaxMessagesResource(object):
    def __init__(self):
        self.logger = logging.getLogger('kizuna_api.' + __name__)

    # todo: put me in a middleware
    def on_get(self, req, resp):
        if not valid_auth_header(req.auth):
            resp.status = falcon.HTTP_401
            return

        with db_session_scope(make_session) as session:
            messages = session \
                .query(FaxMessage) \
                .filter(FaxMessage.printed_at.is_(None)) \
                .order_by(asc(FaxMessage.created_at)) \
                .all()

            resp.body = json.dumps({'messages': [m.to_json_serializable() for m in messages]})


class FaxMessageResource(object):
    def on_put(self, req, resp, message_id):
        # todo: put me in a middleware
        if not valid_auth_header(req.auth):
            resp.status = falcon.HTTP_401
            return

        message_id = int(message_id)

        data = json.load(req.stream)

        with db_session_scope(make_session) as session:
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


app = falcon.API()

app.req_options.auto_parse_form_urlencoded = True

events = EventsResource()
app.add_route('/slack/events', events)

slash_commands = SlashCommandsResource()
app.add_route('/slack/slash_commands', slash_commands)

fax_messages = FaxMessagesResource()
app.add_route('/fax_messages', fax_messages)

fax_message = FaxMessageResource()
app.add_route('/fax_messages/{message_id}', fax_message)

healthChecks = HealthCheckResource()
app.add_route('/', healthChecks)
