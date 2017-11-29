import re


class Command:
    def __init__(self, name, pattern, help_text='', is_at=True) -> None:
        self.name = name
        self.is_at = is_at
        self.pattern = pattern
        self.help_text = help_text
        self.pattern = re.compile(pattern, re.IGNORECASE) if type(pattern) is str else pattern

    def help(self, bot_name):
        return self.help_text.replace("{bot}", bot_name)

    @staticmethod
    def send(slack_client, channel, text):
        return slack_client.api_call("chat.postMessage",
                                     channel=channel,
                                     text=text,
                                     as_user=True)

    def respond(self, slack_client, message, matches):
        return None

    def maybe_respond(self, slack_client, message):
        match = self.pattern.match(message['text'])
        if bool(match):
            return self.respond(slack_client, message, match.groups())
