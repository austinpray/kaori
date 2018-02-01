import re


def format_slack_mention(slack_id: str):
    return f"<@{slack_id}>"


user_id_regex = '^<@(U[A-Za-z0-9]{8,})>$'


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
