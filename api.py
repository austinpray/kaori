import falcon
import json
import config
import logging

from worker import worker


class HealthCheckResource(object):
    def on_get(self, req, resp):
        resp.body = '{"ok": true}'


class EventsResource(object):

    def __init__(self):
        self.logger = logging.getLogger('thingsapp.' + __name__)

    def on_post(self, req, resp):
        if not req.content_length:
            resp.status = falcon.HTTP_400
            resp.body = 'go away'
            return

        doc = json.load(req.stream)
        print(doc)

        callback_type = doc['type']

        if doc['token'] != config.SLACK_VERIFICATION_TOKEN:
            resp.status = falcon.HTTP_401
            resp.body = 'go away'
            return

        if callback_type == 'url_verification':
            resp.body = doc['challenge']
            return

        if callback_type == 'event_callback':
            event = doc['event']
            event_type = event['type']
            if event_type == 'message':
                self.logger.debug(event)
                worker.send(event)

        resp.body = 'thanks!'


app = falcon.API()

events = EventsResource()
app.add_route('/slack/events', events)

healthChecks = HealthCheckResource()
app.add_route('/', healthChecks)
