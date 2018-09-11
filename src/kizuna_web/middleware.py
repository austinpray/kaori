from functools import wraps

from flask import request, session, render_template

from src.kizuna import User


def check_auth(token):
    """This function is called to check if a username /
    password combination is valid.
    """
    try:
        token = User.decrypt_token(token)
        return token and len(token) > 0
    except InvalidToken:
        return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return render_template('not_authorized.jinja2'), 401


def requires_auth_factory(app):
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.values.get('auth')
            if not auth or not check_auth(auth):
                if 'auth' not in session:
                    return authenticate()

                if not check_auth(session['auth']):
                    return authenticate()

            if auth:
                session['auth'] = auth
            return f(*args, **kwargs)

        return decorated

    return requires_auth
