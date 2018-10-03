import re
from abc import ABC, abstractmethod
from functools import partial
from types import SimpleNamespace
from typing import Pattern, Callable

from slackclient import SlackClient
from slacktools.chat import send, send_ephemeral
from slacktools.message import format_slack_mention

from kizuna.support.strings import KIZUNA
from kizuna.support.utils import strip_tokens
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

            user_id = self.client.api_call('auth.test').get('user_id')
            if not user_id:
                raise RuntimeError('no user_id')

            self._cached_bot_id = user_id

        return self._cached_bot_id

    @staticmethod
    def make_mention_token(token: str) -> Pattern:
        return re.compile(token, re.IGNORECASE)

    @property
    def mention_tokens(self):
        return (
            self.make_mention_token(re.escape(format_slack_mention(self.id))),
            self.make_mention_token('@?kazu?(?:ha)?'),
            self.make_mention_token(f'@?{re.escape("カズハ")}'),
            self.make_mention_token(f'@?{re.escape("かずは")}'),
            self.make_mention_token(f'@?{re.escape("和葉")}'),
            # old kizuna name
            self.make_mention_token('@?kiz(?:una)?'),
            self.make_mention_token(f'@?{re.escape(KIZUNA)}'),
        )

    @property
    def mentioned(self) -> SimpleNamespace:
        ns = SimpleNamespace()

        def anywhere(token: Pattern, text: str):
            return token.search(text)

        def directly(token: Pattern, text: str):
            return token.match(text)

        ns.anywhere = partial(self.mentioned_by, self.mention_tokens, anywhere)
        ns.directly = partial(self.mentioned_by, self.mention_tokens, directly)

        return ns

    @staticmethod
    def mentioned_by(tokens, fn: Callable, text: str) -> bool:
        for token in tokens:
            if fn(token, text):
                return True

        return False

    def addressed_by(self, message: SlackMessage):
        if message.user == self.id:
            return False

        return self.mentioned.directly(message.text)

    def understands(self, message: SlackMessage, with_pattern: Pattern):
        return with_pattern.match(strip_tokens(self.mention_tokens, message.text.strip()))

    def respond(self, message: SlackMessage, text: str):
        send(self.client, message.channel, text)

    def reply(self, message: SlackMessage, text: str, ephemeral: bool = False):
        text_with_mention = f'{format_slack_mention(message.user)} {text}'
        if ephemeral:
            return send_ephemeral(self.client, message.channel, message.user, text_with_mention)

        return send(self.client, message.channel, text_with_mention)
