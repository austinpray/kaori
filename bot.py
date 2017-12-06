import os
import signal
import sys
import time
import traceback
import backoff
from sqlalchemy.exc import OperationalError as DatabaseOperationalError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from slackclient import SlackClient
from slackclient.server import SlackConnectionError
from requests import ConnectionError

from kizuna.Kizuna import Kizuna
from kizuna.commands.AtGraphCommand import AtGraphCommand
from kizuna.commands.AtGraphDataCollector import AtGraphDataCollector
from kizuna.commands.ClapCommand import ClapCommand
from kizuna.commands.PingCommand import PingCommand
from kizuna.commands.ReactCommand import ReactCommand
from kizuna.commands.UserRefreshCommand import UserRefreshCommand
from kizuna.strings import HAI_DOMO, GOODBYE

from raven import Client
import config


def signal_handler(signal, frame):
    print("\n{}".format(GOODBYE))
    sys.exit(0)


READ_WEBSOCKET_DELAY = 0.01

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    DEV_INFO = Kizuna.read_dev_info('./.dev-info.json')

    sentry = Client(config.SENTRY_URL,
                    release=DEV_INFO.get('revision'),
                    environment=config.KIZUNA_ENV) if config.SENTRY_URL else None

    if not config.SLACK_API_TOKEN:
        raise ValueError('You are missing a slack token! Please set the SLACK_API_TOKEN environment variable in your '
                         '.env file or in the system environment')

    main_loop_exceptions = (DatabaseOperationalError,
                            ConnectionError,
                            SlackConnectionError)

    def on_backoff(details):
        print("Ran into trouble in the main_loop monkaS. "
              "Backing off {wait:0.1f} seconds after {tries} tries ".format(**details))

        if sentry:
            sentry.captureException()
        else:
            print(traceback.format_exc())

    @backoff.on_exception(backoff.expo,
                          main_loop_exceptions,
                          max_tries=8,
                          on_backoff=on_backoff)
    def main_loop():
        sc = SlackClient(config.SLACK_API_TOKEN)

        db_engine = create_engine(config.DATABASE_URL)
        Session = sessionmaker(bind=db_engine)

        if sc.rtm_connect():
            auth = sc.api_call('auth.test')
            bot_id = auth['user_id']

            k = Kizuna(bot_id,
                       slack_client=sc,
                       main_channel=config.MAIN_CHANNEL,
                       home_channel=config.KIZUNA_HOME_CHANNEL)

            k.handle_startup(DEV_INFO, Session())

            pc = PingCommand()
            k.register_command(pc)

            clap = ClapCommand()
            k.register_command(clap)

            at_graph_command = AtGraphCommand(Session)
            k.register_command(at_graph_command)

            at_graph_data_collector = AtGraphDataCollector(Session, sc)
            k.register_command(at_graph_data_collector)

            user_refresh_command = UserRefreshCommand(db_session=Session)
            k.register_command(user_refresh_command)

            react_command = ReactCommand()
            k.register_command(react_command)

            print("{} BOT_ID {}".format(HAI_DOMO, bot_id))

            while True:
                read = sc.rtm_read()
                try:
                    if read:
                        for output in read:
                            if output['type'] == 'message':
                                k.handle_message(output)
                except Exception:
                    if sentry:
                        sentry.captureException()
                    else:
                        print(traceback.format_exc())

                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Can't connect to slack.")

    main_loop()
