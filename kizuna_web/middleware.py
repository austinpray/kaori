from functools import wraps
from flask import request, Response
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


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.values.get('auth')
        if not auth or not check_auth(auth):
            return authenticate()
        return f(*args, **kwargs)
    return decorated