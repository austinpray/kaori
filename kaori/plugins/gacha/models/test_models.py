import re
from pathlib import Path
from unittest.mock import Mock

from kaori.plugins.users import User

from kaori.skills import LocalFileUploader

from kaori.adapters.slack import SlackMessage, SlackAdapter
from .Image import Image
import os
from uuid import uuid4


def test_image_from_slack():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    db_engine = create_engine(os.getenv('DATABASE_URL'))
    make_session = sessionmaker(bind=db_engine)

    session = make_session()

    image_file = Path(__file__) \
        .parent \
        .joinpath('../../../../tests/fixtures/kaori.png') \
        .resolve()

    file = {
        'id': 'ZZZ'
    }

    slack_user = str(uuid4())

    message = SlackMessage({
        'event': {
            'user': slack_user,
            'files': [file],
        },
    })

    user = User(name=str(uuid4()),
                slack_id=slack_user,
                api_key=str(uuid4()))

    session.add(user)
    session.commit()

    def fake_downloader(*args, **kwargs):
        return 'fake.png', image_file.open('rb')

    img = Image.from_slack_message(message=message,
                                   session=session,
                                   slack_adapter=Mock(spec=SlackAdapter,
                                                      client=None),
                                   uploader=LocalFileUploader(),
                                   slack_file_downloader=fake_downloader)

    session.add(img)
    session.commit()

    assert re.match(r'https://kaori-img.ngrok.io/fake-sha512-\S+.png', img.url) is not None
    assert img.owner == user.id
