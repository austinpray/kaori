from abc import ABC, abstractmethod

import re
from slackclient import SlackClient
from slacktools.chat import send
from slacktools.message import format_slack_mention
from typing import Pattern, Tuple

from kizuna.support.strings import KIZUNA
from . import Adapter


class SlackEvent:
    def __init__(self, payload) -> None:
        self.team_id = payload.get('team_id')
        event = payload.get('event')
        self.type = event.get('type')
        self.user = event.get('user')
        self.ts = event.get('ts')
        self.text = event.get('text')
        self.item = event.get('item')

    @staticmethod
    def create_from(payload):
        type = payload.get('event', {}).get('type')
        if type == 'message':
            return SlackMessage(payload)

        return SlackEvent(payload)


class SlackMessage(SlackEvent):
    def __init__(self, payload) -> None:
        super().__init__(payload)
        event = payload.get('event')
        self.channel = event.get('channel')
        self.text: str = event.get('text')


class SlackCommand(ABC):

    @staticmethod
    @abstractmethod
    async def handle(*args, **kwargs):
        raise NotImplementedError


class SlackAdapter(Adapter):
    def __init__(self, slack_client: SlackClient) -> None:
        super().__init__()
        self.client = slack_client
        self._cached_bot_id = None

    handles = {SlackCommand}
    provides = {SlackMessage}

    @staticmethod
    def convert_payload(payload):
        return SlackEvent.create_from(payload)

    @property
    def id(self) -> str:
        if not self._cached_bot_id:

            id = self.client.api_call('auth.test').get('user_id')
            if not id:
                raise RuntimeError('no user_id')

            self._cached_bot_id = id

        return self._cached_bot_id

    @property
    def respond_tokens(self) -> Tuple[str, Pattern]:
        return (
            re.compile('@?kiz(?:una)?', re.IGNORECASE),
            format_slack_mention(self.id),
            KIZUNA
        )

    def addressed_by(self, message: SlackMessage):
        for token in self.respond_tokens:
            if isinstance(token, str) and message.text.startswith(token):
                return True

            if token.match(message.text):
                return True

        return False

    def respond(self, message: SlackMessage, text: str):
        send(self.client, message.channel, text)

    def reply(self, message: SlackMessage, text: str):
        send(self.client, message.channel, f'{format_slack_mention(message.user)} {text}')
