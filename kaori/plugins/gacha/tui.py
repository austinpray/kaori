from typing import List

import random
from .engine import NatureName, RarityName
from .models.Card import Card
from .utils import tmp_prefix
from slacktools.message import format_url

_default_image = "https://storage.googleapis.com/img.kaori.io/static/present.png"

_readme_url = 'https://github.com/austinpray/kaori/blob/master/kaori/plugins/gacha/README.md'

_readme_link = f"<{_readme_url}|README>"

_card_guide_link = f'<{_readme_url}#card-guide|Card Guide>'

def card_meta_block(card: Card, with_image=True):
    block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": '\n'.join([
                f"*{'(no name)' if card.name.startswith(tmp_prefix) else card.name}*",
                f"_{card.engine.subtitle}_" if card.engine else '(stats pending)',
                card.description if card.description else '_(no description)_'
            ])
        },
    }

    if with_image:
        block['accessory'] = {
            "type": "image",
            "image_url": card.image.url if card.image else _default_image,
            "alt_text": card.name if not card.description else card.description
        }

    return block


def render_card(card: Card, preview_header=False) -> dict:
    blocks = [
        {
            "type": "image",
            "image_url": card.image.url if card.image else _default_image,
            "alt_text": card.name if not card.description else card.description
        },
        card_meta_block(card, with_image=False),
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
                    "text": f"*Clown:* {card.clown}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Horny:* {card.horny}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Cursed:* {card.cursed}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Feral:* {card.feral}"
                },
            ],
        },
    ]

    if preview_header:
        blocks = [
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
            *blocks,
        ]

    return {
        'blocks': blocks
    }


def instructions_blocks(bot_name: str) -> List[dict]:
    bullets = [
        f"• To avoid a fiasco *I will only respond to direct mentions* and I will only respond to you.",
        f"• *To quit card creation* just send `{bot_name} quit`",
        f"• *To start over* just send `{bot_name} start over`",
        # TODO: beta notice
        "• *Beta Notice:* cards are currently free to create.",
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
    prices = [
        {
            "type": "mrkdwn",
            # "text": f"*{rank}:* {price} kkreds",
            "text": f"*{rank}:* ~{price} kkreds~ _free_",
        } for rank, price in Card.rarity_prices().items()
    ]
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Card price breakdown by rarity:"
            }
        },
        {
            "type": "section",
            "fields": prices,
        },
    ]


def card_index_blocks(cards: List[Card]):
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_Card creation is free during the beta_",
            }
        },
    ]


def card_index_blocks(cards: List[Card]):
    return [
        card_meta_block(card) for card in cards
    ]


def help_blocks():
    gacha_jpg = "https://raw.githubusercontent.com/austinpray/kaori/master/kaori/plugins/gacha/static/img/gacha.jpg"
    commands = [
        'Create a card: `kaori create card`',
        'List your cards: `kaori show cards`',
        'Show a full card: `kaori show card NAME`',
        'Battle cards: `kaori battle NAME vs. NAME`',
        'Show card creation prices: `kaori card prices`',
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
    examples = get_nature_examples()
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Choose two natures for your card (ex. `@kaori stupid baby` or `@kaori feral horny`)"
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
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Choose two natures for your card.*\n(ex. {' or '.join(examples)})"
            },
        },
    ]


def get_nature_examples():
    examples = [
        f"`@kaori {' '.join(random.sample([str(n) for n in NatureName], 2))}`"
        for _ in range(2)
    ]
    return examples


def query_rarity_blocks():
    return [
        *price_blocks(),
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*What rarity would you like your card to be?*\n"
                        "(ex. `@kaori C`)"
            },
        },
    ]


def battle_blocks(attacker: Card, defender: Card, battle_url: str):
    return [
        card_meta_block(attacker),
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "🆚"
            },
        },
        card_meta_block(defender),
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Let's go!"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Start Battle",
                },
                "style": "primary",
                "url": battle_url,
            }
        },
    ]


def create_are_you_sure_blocks(card):
    return [
        *render_card(card)['blocks'],
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                # TODO beta notice
                "text": f"~This card will cost {card.price()} kkreds~ "
                        "Cards are free to create during the beta!\n"
                        "*Are you sure you want to create this card?*\n"
                        "(ex. `@kaori yes`)"
            },
        },
    ]
