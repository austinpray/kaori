from contextlib import contextmanager
from urllib.parse import urlparse, urlencode, urlunparse


def build_url(baseurl, path, args_dict=None):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urlparse(baseurl))
    url_parts[2] = path
    if args_dict:
        url_parts[4] = urlencode(args_dict)
    return urlunparse(url_parts)


def strip_tokens(tokens, message: str):
    message = message.strip()
    for token in tokens:
        match = token.match(message)
        if match:
            return message[match.end(0):].strip()


@contextmanager
def db_session_scope(session_maker):
    if not session_maker:
        raise RuntimeError('no db_session_maker specified for this command')

    session = session_maker()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def linear_scale(old_max, old_min, new_max, new_min, value):
    old_range = (old_max - old_min)
    if old_range == 0:
        return value
    new_range = (new_max - new_min)
    return (((value - old_min) * new_range) / old_range) + new_min
