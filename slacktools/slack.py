import re
from argparse import ArgumentParser
from functools import partial

from kizuna.models import User


def format_slack_mention(slack_id: str):
    return f"<@{slack_id}>"


user_id_regex = '^<@(U[A-Za-z0-9]{8,})>$'


def extract_mentions(text):
    return set(re.findall(r"<@(\S+)>", text, re.DOTALL))


def get_user_id_from_mention(m: str):
    match = re.match(user_id_regex, m)
    if not match:
        return None

    return match.group(1)


def is_user_mention(s: str) -> bool:
    """user mentions should be in format <@UXXXXXXXX>"""

    if not s or not re.match(user_id_regex, s):
        return False

    return True


def send(slack_client, channel, text):
    return slack_client.api_call("chat.postMessage",
                                 channel=channel,
                                 text=text,
                                 as_user=True)


def reply(slack_client, message, text):
    return slack_client.api_call("chat.postMessage",
                                 channel=message['channel'],
                                 text=f"{format_slack_mention(message['user'])} {text}",
                                 as_user=True)


def send_factory(slack_client, channel):
    return partial(send, slack_client, channel)


def send_ephemeral(slack_client, channel, user, text):
    if isinstance(user, User):
        user = user.slack_id

    return slack_client.api_call("chat.postEphemeral",
                                 channel=channel,
                                 user=user,
                                 text=text,
                                 as_user=True)


def send_ephemeral_factory(slack_client, channel, user):
    return partial(send_ephemeral, slack_client, channel, user)


class SlackArgumentParserException(Exception):
    pass


class SlackArgumentParser(ArgumentParser):
    def error(self, message):
        raise SlackArgumentParserException(message)


def slack_link(text, url):
    return '<{}|{}>'.format(url, text)
