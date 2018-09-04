from urllib.parse import urlparse, urlencode, urlunparse
from contextlib import contextmanager


def build_url(baseurl, path, args_dict=None):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urlparse(baseurl))
    url_parts[2] = path
    if args_dict:
        url_parts[4] = urlencode(args_dict)
    return urlunparse(url_parts)


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
