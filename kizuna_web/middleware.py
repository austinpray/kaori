from functools import wraps
from flask import request, Response, session
from kizuna.models.User import User, InvalidToken


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
    return Response("<h1>Not Authorized</h1><p>Your token is expired or you didn't give me a token", status=401)


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
