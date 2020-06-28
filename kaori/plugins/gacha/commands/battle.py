import re
from typing import Optional, Match

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter
from kaori.skills import DB
from ..models.Card import Card
from ..skills import CardBattler
from ..tui import battle_blocks


def _user_requesting_battle(message: SlackMessage, bot: SlackAdapter) -> Optional[Match]:
    pattern = re.compile(r'battle\s+(.+)\s+vs?\.?\s+(.+)', re.I)
    return bot.understands(message, with_pattern=pattern)


class CardBattleCommand(SlackCommand):
    """usage: {bot} battle {name} vs. {name}"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB, battler: CardBattler):
        if not bot.addressed_by(message):
            return

        requested_battle = _user_requesting_battle(message=message,
                                                   bot=bot)

        if not requested_battle:
            return

        attacker_search = requested_battle[1]
        defender_search = requested_battle[2]

        with db.session_scope() as session:

            attacker = Card.search_for_one(session, attacker_search)

            if not attacker:
                bot.reply(message, f'no card named "{attacker_search}"', create_thread=True)
                return

            defender = Card.search_for_one(session, defender_search)

            if not defender:
                bot.reply(message, f'no card named "{defender_search}"', create_thread=True)
                return

            battle_url = battler.get_battle_url(attacker.engine, defender.engine)
            bot.reply(message,
                      create_thread=True,
                      blocks=battle_blocks(attacker=attacker,
                                           defender=defender,
                                           battle_url=battle_url))
