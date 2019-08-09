def valid_auth_header(api_key, auth_header) -> bool:
    if not auth_header:
        return False

    auth_token = auth_header.split(' ')[1]

    if not auth_token or auth_token != api_key:
        return False

    return True
