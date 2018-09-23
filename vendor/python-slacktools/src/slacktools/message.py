import re
from typing import Set, List, Union

from .util import _multiple_replace

user_id_regex = r'<@(U[A-Za-z0-9]{8,})>'


def slack_escape(text: str) -> str:
    """
    Escape slack control sequences in a string
    https://api.slack.com/docs/message-formatting#how_to_escape_characters

    >>> slack_escape('Hello & <world> 🌊')
    'Hello &amp; &lt;world&gt; 🌊'
    """
    return _multiple_replace(text, {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
    })


def format_slack_mention(slack_id: str):
    """
    Formats a slack user ID as a mention using slack control sequences
    https://api.slack.com/docs/message-formatting#linking_to_channels_and_users

    >>> format_slack_mention('U5H9UR207')
    '<@U5H9UR207>'
    """
    return "<@{}>".format(slack_id)


def format_channel_link(name: str, channel_id: str):
    """
    Formats a channel name and ID as a channel link using slack control sequences
    https://api.slack.com/docs/message-formatting#linking_to_channels_and_users

    >>> format_channel_link('general', 'C024BE7LR')
    '<#C024BE7LR|general>'
    """
    return '<#{}|{}>'.format(channel_id, name)


def format_url(text, url):
    """
    Formats an inline slack hyperlink to a URL
    https://api.slack.com/docs/message-formatting#linking_to_urls

    >>> format_url('my website', 'https://austinpray.com')
    '<my website|https://austinpray.com>'
    """
    return '<{}|{}>'.format(slack_escape(text), url)


def extract_mentions(text: str) -> List[str]:
    """Returns a list of slack user ID strings in the order that they appear in the string

    >>> extract_mentions('waddup <@U5H9UR207> testing <@U8DCV8P6X>')
    ['U5H9UR207', 'U8DCV8P6X']
    >>> extract_mentions('hey <@U5GJR5GF7> test this yooo <@U5GJR5GF7>')
    ['U5GJR5GF7', 'U5GJR5GF7']
    >>> extract_mentions('<@U5GJR5GF7><@U5H9UR207><@U5GJR5GF7>')
    ['U5GJR5GF7', 'U5H9UR207', 'U5GJR5GF7']
    """
    return re.findall(user_id_regex, text, re.DOTALL)


def extract_unique_mentions(text: str) -> Set[str]:
    """Returns a set of slack user ID strings

    >>> extract_unique_mentions('hey <@U5GJR5GF7> test this yooo <@U5GJR5GF7>')
    {'U5GJR5GF7'}
    >>> extract_unique_mentions('waddup <@U5H9UR207> testing <@U8DCV8P6X>') - {'U8DCV8P6X', 'U5H9UR207'}
    set()
    """
    return set(extract_mentions(text))


def extract_user_id_from_mention(m: str) -> Union[str, None]:
    """Given a slack mention control sequence extract the

    >>> extract_user_id_from_mention('<@U5H9UR207>')
    'U5H9UR207'
    >>> extract_user_id_from_mention('ayy') is None
    True
    """
    match = re.match(user_id_regex, m)
    if not match:
        return None

    return match.group(1)


def is_user_mention(s: str) -> bool:
    """tests if a string is a user mention control sequence

    >>> is_user_mention('<@UXXXXXXXX>')
    True
    >>> is_user_mention('<@UXX>')
    False
    """
    if not s or not re.match(user_id_regex, s):
        return False

    return True
