import ujson as json

from falcon import Response


class HealthCheckResource(object):
    def on_get(self, req, resp: Response):
        resp.body = json.dumps({'ok': True})
