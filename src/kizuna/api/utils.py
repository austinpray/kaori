import config


def valid_auth_header(auth_header) -> bool:
    if not auth_header:
        return False

    auth_token = auth_header.split(' ')[1]

    if not auth_token or auth_token != config.API_KEY:
        return False

    return True
