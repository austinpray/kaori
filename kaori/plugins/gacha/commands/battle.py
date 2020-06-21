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
        attacker_slug = Card.sluggify_name(attacker_search)
        defender_search = requested_battle[2]
        defender_slug = Card.sluggify_name(defender_search)

        with db.session_scope() as session:

            attacker = session.query(Card) \
                .filter(Card.published == True) \
                .filter(Card.slug.ilike(f'%{attacker_slug}%')) \
                .first()

            if not attacker:
                bot.reply(message, f'no card named "{attacker_search}"', create_thread=True)
                return


            defender = session.query(Card) \
                .filter(Card.published == True) \
                .filter(Card.slug.ilike(f'%{defender_slug}%')) \
                .first()

            if not defender:
                bot.reply(message, f'no card named "{defender_search}"', create_thread=True)
                return

            battle_url = battler.get_battle_url(attacker.engine, defender.engine)
            bot.reply(message,
                      create_thread=True,
                      blocks=battle_blocks(battle_url=battle_url))
