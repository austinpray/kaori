import importlib.util
import os

import falcon
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .events import EventsResource
from .fax_messages import FaxMessagesResource, FaxMessageResource
from .health_checks import HealthCheckResource
from .slash_commands import SlashCommandsResource

spec = importlib.util.spec_from_file_location("config.kaori", os.path.join(os.getcwd(), 'config/kaori.py'))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

if hasattr(config, 'SENTRY_URL') and config.SENTRY_URL:  # pragma: no cover
    import sentry_sdk

    sentry_sdk.init(dsn=config.SENTRY_URL,
                    environment=config.KIZUNA_ENV)

db_engine = create_engine(config.DATABASE_URL)
make_session = sessionmaker(bind=db_engine)

rabbitmq_broker = RabbitmqBroker(url=config.RABBITMQ_URL)

app = falcon.API()

app.req_options.auto_parse_form_urlencoded = True

events = EventsResource(config, rabbitmq_broker)
app.add_route('/slack/events', events)

slash_commands = SlashCommandsResource(config, make_session)
app.add_route('/slack/slash_commands', slash_commands)

fax_messages = FaxMessagesResource(config, make_session)
app.add_route('/fax_messages', fax_messages)

fax_message = FaxMessageResource(config, make_session)
app.add_route('/fax_messages/{message_id}', fax_message)

healthChecks = HealthCheckResource()
app.add_route('/', healthChecks)
