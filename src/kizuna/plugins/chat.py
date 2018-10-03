import random
import re
from typing import List, Pattern

from kizuna.adapters.slack import SlackCommand, SlackMessage, SlackAdapter


def to_pattern(strings: List[str]) -> Pattern:
    pattern = '|'.join(strings)
    return re.compile(pattern, re.I)


greeting = to_pattern([
    '(?:hi|h[e|u]llo)(?: there)?',
    'waddup',
    "what['|’]?s up",
])

greeting_response = [
    'Hello!',
    'はいども！',
]

interrogative_greeting = to_pattern([
    'how are [you|ya](?: doing)?(?: today)?'
])

interrogative_greeting_response = [
    'Doing just fine',
    'Doing just fine, thanks for asking'
    '悪くないです',
    '絶好調です',
]

im_here_response = [
    'I’m here.',
    'Need something?',
    'Yeah?'
]


class GreetingCommand(SlackCommand):
    """kizuna says hi back"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter):
        if message.user == bot.id:
            return

        text = message.text.strip()
        tokens = text.split()
        if not text:
            return

        if bot.mentioned.directly(tokens[0]) and tokens[0].endswith('?'):
            bot.reply(message, random.choice(im_here_response))

        if interrogative_greeting.search(text) and bot.mentioned.anywhere(text):
            return bot.reply(message, random.choice(interrogative_greeting_response))

        if greeting.search(text) and bot.mentioned.anywhere(text):
            return bot.reply(message, random.choice(greeting_response))
