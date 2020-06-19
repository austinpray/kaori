from typing import List

from .engine import NatureName, RarityName
from .models.Card import Card
from .utils import tmp_prefix

_default_image = "https://storage.googleapis.com/img.kaori.io/static/present.png"

_readme_url = 'https://github.com/austinpray/kaori/blob/master/kaori/plugins/gacha/README.md'

_readme_link = f"<{_readme_url}|README>"

_card_guide_link = f'<{_readme_url}#card-guide|Card Guide>'


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
                        f"_{card.engine.subtitle}_" if card.engine else '(stats pending)',
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
                        "text": f"*Rarity:* {card.rarity_string()}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Max HP:* {card.engine.max_hp}" if card.engine else '?'
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
        f"• To avoid a fiasco *I will only respond to direct mentions* and I will only respond to you.",
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
        # TODO: beta notice
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Beta Notice:* cards are currently free to create. They might be cleared from the database "
                        "at some point when the beta period ends."
            },
        },
    ]


def price_blocks():
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Card price breakdown by rank:",
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*{rank}:* {price} kkreds"
                } for rank, price in Card.rarity_prices().items()
            ]
        },
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


def query_nature_blocks():
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Choose two natures for your card (ex. `stupid baby` or `feral horny`)"
            },
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"• {n}"
                } for n in NatureName
            ]
        },
    ]


def query_rarity_blocks():
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "What rarity would you like your card to be? This will impact how expensive your card will be "
                        "to create."
            },
        },
        # TODO: beta notice
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Beta Notice:* card creation is free at the moment. You will not be charged."
            },
        },
        *price_blocks(),
    ]
