from typing import List

from .models.Card import Card
from .utils import tmp_prefix

_default_image = "https://storage.googleapis.com/img.kaori.io/static/present.png"


def render_card(card: Card) -> dict:
    return {
        'blocks': [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*:mag_right: Card Preview*".upper()
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": '\n'.join([
                        f"*{'(no name)' if card.name.startswith(tmp_prefix) else card.name}*",
                        card.description if card.description else '_(no description)_'
                    ])
                },
                "accessory": {
                    "type": "image",
                    "image_url": card.image.url if card.image else _default_image,
                    "alt_text": card.name if not card.description else card.description
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Rarity:* {card.rarity}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*HP:* {card.hit_points}"
                    },
                ]
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Stupid:* {card.stupid}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Baby:* {card.baby}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Cursed:* {card.cursed}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Horny:* {card.horny}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Clown:* {card.clown}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Feral:* {card.feral}"
                    },
                ],
            },
        ]
    }


def instructions_blocks(bot_name: str) -> List[dict]:
    bullets = [
        "• To avoid a fiasco *I will only respond to direct mentions* and I will only respond to you.",
        f"• *To quit card creation* just send `{bot_name} quit`",
        f"• *To start over* just send `{bot_name} start over`",
    ]

    return [

        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Ok! Let's go! I'm gonna ask you a series of questions in this thread."
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": '\n'.join(bullets)
            }
        },
    ]


def price_blocks():
    return [
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*{rank}:* {price}"
                } for rank, price in Card.rarity_prices().items()
            ]
        }
    ]


def card_index_blocks(cards: List[Card]):
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{card.name}*\n"
            },
            "accessory": {
                "type": "image",
                "image_url": card.image.url if card.image else _default_image,
                "alt_text": card.name if not card.description else card.description
            }
        } for card in cards
    ]


def help_blocks():
    gacha_jpg = "https://raw.githubusercontent.com/austinpray/kaori/master/kaori/plugins/gacha/static/img/gacha.jpg"
    commands = [
        'Create a card: `kaori create card`',
        'List your cards: `kaori show cards`',
        'Show a full card: `kaori show card NAME`',
    ]
    commands = "\n".join([f'• {command}' for command in commands])
    return [
        {
            "type": "image",
            "image_url": gacha_jpg,
            "alt_text": "a gacha machine in japan"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Gacha Card Game*\ncreate, collect, battle gacha cards."
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "For information about the game itself: see the "
                        "<https://github.com/austinpray/kaori/blob/master/kaori/plugins/gacha/README.md|README>"
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f'Available commands:\n{commands}'
            },
        },
    ]
