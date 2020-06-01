from __future__ import annotations

from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session

from kaori.adapters.slack import SlackMessage, SlackAdapter
from kaori.support.models.Models import Base
from kaori.plugins.users import User, UserNotFound
from kaori.skills import FileUploader

from kaori.support.slack_files import download_slack_file


class Image(Base):
    __tablename__ = 'images'

    id = sa.Column('id', sa.Integer, primary_key=True)
    created_at = sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp())

    url = sa.Column('url', sa.Text, nullable=False)
    slack_file_id = sa.Column('slack_file_id', sa.Text)

    owner = sa.Column('owner', sa.Integer, sa.ForeignKey('users.id'), nullable=False)

    @staticmethod
    def from_slack_message(message: SlackMessage,
                           session: Session,
                           slack_adapter: SlackAdapter,
                           uploader: FileUploader) -> Image:
        file = message.files[0]

        if not file:
            raise RuntimeError('no file in message')

        user = User.get_by_slack_id(session, message.user)
        if not user:
            raise UserNotFound('no user, try refreshing users')

        name, downloaded_file = download_slack_file(file['id'], slack_client=slack_adapter.client)
        url = uploader.upload(name, downloaded_file)

        return Image(slack_file_id=file['id'],
                     owner=user.id,
                     url=url)

    def __repr__(self):
        return f"<Img (id='{self.id}', url='{self.url}' owner='{self.owner}')>"
