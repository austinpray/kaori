from time import time
import hmac
from hashlib import sha256

class SignatureVersionException(ValueError): pass

def verify_request(slack_signing_secret: str, timestamp: int, body: str, slack_signature: str):
    """https://api.slack.com/docs/verifying-requests-from-slack"""

    if not slack_signing_secret:
        raise ValueError('slack_signing_secret not provided')
    if not timestamp or not isinstance(timestamp, int):
        raise ValueError('timestamp is not good int')
    if not body:
        raise ValueError('body not provided')
    if not slack_signature:
        raise ValueError('signature not provided')
    if not slack_signature.startswith('v0'):
        raise SignatureVersionException(f"expected the signature to be version 'v0' but got '{slack_signature[:2]}'")

    if abs(time() - timestamp) > 60 * 5:
        # The request timestamp is more than five minutes from local time.
        # It could be a replay attack, so let's ignore it.
        return False

    sig_basestring = f"v0:{timestamp}:{body}"

    my_signature = 'v0=' + hmac.new(
        slack_signing_secret.encode(),
        sig_basestring.encode(),
        sha256
    ).hexdigest()

    print(slack_signature)
    print(my_signature)

    return hmac.compare_digest(my_signature, slack_signature)
