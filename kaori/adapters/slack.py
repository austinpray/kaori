import re
from abc import ABC, abstractmethod
from functools import partial
from types import SimpleNamespace
from typing import Pattern, Callable, Optional

from slackclient import SlackClient
from slacktools.chat import send, send_ephemeral
from slacktools.message import format_slack_mention

from kaori.support.utils import strip_tokens
from . import Adapter


class SlackEvent:
    def __init__(self, payload) -> None:
        self.team_id = payload.get('team_id')
        event = payload.get('event')
        self.type = event.get('type')
        self.user = event.get('user')
        self.text = event.get('text')
        self.item = event.get('item')

        # threading
        self.ts = event.get('ts')
        self.thread_ts = event.get('thread_ts')

        """
        ## Spotting threads
        <https://api.slack.com/messaging/retrieving#finding_threads>
        
        There's a few steps involved with spotting a thread and then
        understanding the context of a message within it. Let's unspool them:

        1. Detect a threaded message by looking for a thread_ts value in the message
        object. The existence of such a value indicates that the message is part of a
        thread.
        2. Identify parent messages by comparing the thread_ts and ts values.  If they
        are equal, the message is a parent message.
        3. Threaded replies are also identified by comparing the thread_ts and ts
        values. If they are different, the message is a reply.
        """
        self.is_thread = bool(self.thread_ts)
        self.is_thread_parent = True if self.is_thread and self.ts == self.thread_ts else False
        self.is_thread_reply = True if self.is_thread and self.ts != self.thread_ts else False

    @staticmethod
    def create_from(payload):
        event = payload.get('event', {})
        event_type = event.get('type')
        text = event.get('text')
        if event_type == 'message' and text:
            return SlackMessage(payload)

        return SlackEvent(payload)


class SlackMessage(SlackEvent):
    def __init__(self, payload) -> None:
        super().__init__(payload)
        event = payload.get('event')
        self.channel = event.get('channel')
        self.text: str = event.get('text')
        self.files: Optional[list] = event.get('files')


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
    provides = {SlackMessage, SlackEvent}

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
    def mention_string(self) -> str:
        return format_slack_mention(self.id)

    @property
    def mention_tokens(self):
        return (
            self.make_mention_token(re.escape(format_slack_mention(self.id))),
            # new kaori name
            self.make_mention_token('@?kaori'),
            self.make_mention_token(f'@?{re.escape("かおり")}'),
            self.make_mention_token(f'@?{re.escape("カオリ")}'),
            # old kizuna name
            self.make_mention_token('@?kiz(?:una)?'),
            self.make_mention_token(f'@?{re.escape("きずな")}'),
            self.make_mention_token(f'@?{re.escape("キズナ")}'),
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

    def edit(self,
             message: SlackMessage,
             **kwargs):
        return self.client.api_call('chat.update',
                                    ts=message.ts,
                                    channel=message.channel,
                                    **kwargs)

    def react(self,
              message: SlackMessage,
              reaction: str):
        return self.client.api_call('reactions.add',
                                    name=reaction,
                                    channel=message.channel,
                                    timestamp=message.ts)

    def reply(self,
              message: SlackMessage,
              text: str = '',
              ephemeral: bool = False,
              create_thread: bool = False,
              **kwargs):
        text_with_mention = f'{format_slack_mention(message.user)} {text}' if text else ''
        if ephemeral:
            return send_ephemeral(self.client, message.channel, message.user, text_with_mention)

        thread_ts = None
        if message.is_thread:
            thread_ts = message.thread_ts
        elif create_thread:
            thread_ts = message.ts

        return send(self.client, message.channel, text_with_mention, thread_ts=thread_ts, **kwargs)
