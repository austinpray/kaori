import falcon
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from .events import EventsResource
from .fax_messages import FaxMessagesResource, FaxMessageResource
from .health_checks import HealthCheckResource
from .slash_commands import SlashCommandsResource

db_engine = create_engine(config.DATABASE_URL)
make_session = sessionmaker(bind=db_engine)

rabbitmq_broker = RabbitmqBroker(url=config.RABBITMQ_URL)

app = falcon.API()

app.req_options.auto_parse_form_urlencoded = True

events = EventsResource(rabbitmq_broker)
app.add_route('/slack/events', events)

slash_commands = SlashCommandsResource(make_session)
app.add_route('/slack/slash_commands', slash_commands)

fax_messages = FaxMessagesResource(make_session)
app.add_route('/fax_messages', fax_messages)

fax_message = FaxMessageResource(make_session)
app.add_route('/fax_messages/{message_id}', fax_message)

healthChecks = HealthCheckResource()
app.add_route('/', healthChecks)
