from urllib.parse import urlparse

import ujson
from furl import furl
from ..engine.core.card import Card
from ..engine.core.battle import Battle


class CardBattler:

    def __init__(self, player_url_base: str) -> None:
        self.player_url_base = player_url_base

    def get_battle_url(self, attacker: Card, defender: Card) -> str:
        battle = Battle(attacker, defender).run()
        payload = ujson.dumps(battle.serialize_min())
        player_url = furl(self.player_url_base)
        player_url.args['in'] = payload
        return str(player_url)
