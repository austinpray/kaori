import pytest
from slacktools.authorization import verify_signature, make_signature, SignatureVersionException
from time import time

def test_verify_signature():
    with pytest.raises(ValueError):
        verify_signature(None, 1111, 'string', 'v0=ayy')
    with pytest.raises(ValueError):
        verify_signature('secret', None, 'string', 'v0=ayy')
    with pytest.raises(ValueError):
        verify_signature('secret', 1111, None, 'v0=ayy')
    with pytest.raises(ValueError):
        verify_signature('secret', 1111, 'body', None)
    with pytest.raises(SignatureVersionException):
        verify_signature('secret', 1111, 'body', 'something bogus')

    ss = '8f742231b10e8888abcd99yyyzzz85a5'
    assert verify_signature(signing_secret=ss,
                            request_timestamp=1531420618,
                            body='token=xyzz0WbapA4vBCDEFasx0q6G&team_id=T1DC2JH3J&team_domain=testteamnow&channel_id=G8PSS9T3V&channel_name=foobar&user_id=U2CERLKJA&user_name=roadrunner&command=%2Fwebhook-collect&text=&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT1DC2JH3J%2F397700885554%2F96rGlfmibIGlgcZRskXaIFfN&trigger_id=398738663015.47445629121.803a0bc887a14d10d2c447fce8b6703c',
                            signature='v0=a2114d57b48eac39b9ad189dd8316235a7b4a8d21a10bd27519666489c69b503',
                            current_timestamp=1531420618)

    # bogus key
    assert not verify_signature(signing_secret='bogus',
                            request_timestamp=1531420618,
                            body='token=xyzz0WbapA4vBCDEFasx0q6G&team_id=T1DC2JH3J&team_domain=testteamnow&channel_id=G8PSS9T3V&channel_name=foobar&user_id=U2CERLKJA&user_name=roadrunner&command=%2Fwebhook-collect&text=&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT1DC2JH3J%2F397700885554%2F96rGlfmibIGlgcZRskXaIFfN&trigger_id=398738663015.47445629121.803a0bc887a14d10d2c447fce8b6703c',
                            signature='v0=a2114d57b48eac39b9ad189dd8316235a7b4a8d21a10bd27519666489c69b503',
                            current_timestamp=1531420618)

    # replay attacks
    assert not verify_signature(signing_secret=ss,
                                request_timestamp=1531420618,
                                body='token=xyzz0WbapA4vBCDEFasx0q6G&team_id=T1DC2JH3J&team_domain=testteamnow&channel_id=G8PSS9T3V&channel_name=foobar&user_id=U2CERLKJA&user_name=roadrunner&command=%2Fwebhook-collect&text=&response_url=https%3A%2F%2Fhooks.slack.com%2Fcommands%2FT1DC2JH3J%2F397700885554%2F96rGlfmibIGlgcZRskXaIFfN&trigger_id=398738663015.47445629121.803a0bc887a14d10d2c447fce8b6703c',
                                signature='v0=a2114d57b48eac39b9ad189dd8316235a7b4a8d21a10bd27519666489c69b503',
                                current_timestamp=1531420618 + (60*6))

    t = int(time())
    s1 = make_signature(ss, t, 'ayy lmao')

    assert verify_signature(signing_secret=ss,
                                request_timestamp=t,
                                body='ayy lmao',
                                signature=s1)
