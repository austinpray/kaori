import random
from typing import List

from .engine import NatureName
from .models.Card import Card
from .utils import tmp_prefix

_default_image = "https://storage.googleapis.com/img.kaori.io/static/present.png"

_readme_url = 'https://github.com/austinpray/kaori/blob/master/kaori/plugins/gacha/README.md'

_readme_link = f"<{_readme_url}|README>"

_card_guide_link = f'<{_readme_url}#card-guide|Card Guide>'


def _percent(number) -> str:
    return f'{round(number * 100)}%'


def card_meta_block(card: Card, with_image=True):
    block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": '\n'.join([
                f"*{'(no name)' if card.name.startswith(tmp_prefix) else card.name}*",
                f"_{card.engine.subtitle}_" if card.engine else '(stats pending)',
                "\n",
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


def render_stats_blocks(card: Card) -> List[dict]:
    if not card.is_complete:
        return [{
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"_stats pending..._"
                },
            ]
        }]

    eng = card.engine

    return [
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f'*{title}*\n`{text[0]:<4} {"(" + text[1] + ")":>11}`'
                } for title, text in {
                    'HP':  (eng.max_hp, f'{card.stupid} stupid'),
                    'EVA': (_percent(eng.evasion), f'{card.baby} baby'),
                    'AMR': (eng.armor, f'{card.clown} clown'),
                    'DMG': (eng.dmg, f'{card.horny} horny'),
                    'CRT': (_percent(eng.crit), f'{card.cursed} cursed'),
                    'SPD': (round(eng.speed, 2), f'{card.feral} feral'),
                }.items()
            ],
        },
    ]


def render_card(card: Card, preview_header=False) -> dict:
    stats_blocks = render_stats_blocks(card)
    blocks = [
        {
            "type": "image",
            "image_url": card.image.url if card.image else _default_image,
            "alt_text": card.name if not card.description else card.description
        },
        card_meta_block(card, with_image=False),
        {"type": "divider"},
        *stats_blocks,
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
        'Show card statistics: `kaori card stats`',
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
                    "text": "Watch Battle",
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


def card_stats_blocks(card_total: int):
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"We have a total of {card_total} card{'' if card_total == 1 else 's'} created so far!"
            },
        },
    ]
