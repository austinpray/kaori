from __future__ import annotations

from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session

from kaori.adapters.slack import SlackMessage
from kaori.support.models.Models import Base
from kaori.plugins.users import User, UserNotFound


class Image(Base):
    __tablename__ = 'images'

    id = sa.Column('id', sa.Integer, primary_key=True)
    created_at = sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp())

    url = sa.Column('url', sa.Text, nullable=False)
    slack_file_id = sa.Column('slack_file_id', sa.Text)

    owner = sa.Column('owner', sa.Integer, sa.ForeignKey('users.id'), nullable=False)

    @staticmethod
    def from_slack_message(message: SlackMessage, session: Session) -> Image:
        valid_filetypes = ['jpeg', 'jpg', 'png', 'gif']
        file = message.files[0]
        if file['filetype'] not in valid_filetypes:
            raise RuntimeError(f"Invalid file type {file['filetype']}")

        user = User.get_by_slack_id(session, message.user)
        if not user:
            raise UserNotFound('no user, try refreshing users')

        url = 'https://storage.googleapis.com/img.kaori.io/static/miku.jpg'

        return Image(slack_file_id=file['id'],
                     owner=user.id,
                     url=url)

    def __repr__(self):
        return f"<Img (id='{self.id}', url='{self.url}' owner='{self.owner}')>"
