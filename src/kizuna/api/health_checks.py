class HealthCheckResource(object):
    def on_get(self, req, resp):
        resp.body = '{"ok": true}'
