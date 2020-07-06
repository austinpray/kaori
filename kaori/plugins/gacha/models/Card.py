from __future__ import annotations

import re
from typing import Tuple, Optional, Dict, List, Union

import sqlalchemy as sa
import sqlalchemy.orm
from sqlalchemy.orm import Session

from kaori.support.models.Models import Base
from ..engine import Card as GameCard
from ..engine.core import RarityName, Card as EngineCard, NatureName
from ...users import User


class InvalidCardName(RuntimeError):
    pass


class Card(Base):
    __tablename__ = 'cards'

    id = sa.Column('id', sa.Integer, primary_key=True)
    created_at = sa.Column('created_at', sa.DateTime, default=sa.func.current_timestamp())

    name = sa.Column('name', sa.UnicodeText, nullable=False, unique=True)
    slug = sa.Column('slug', sa.UnicodeText, nullable=False, unique=True)

    # creation related
    owner = sa.Column('owner', sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    published = sa.Column('published', sa.Boolean, nullable=False, default=False)
    creation_thread_channel = sa.Column('creation_thread_channel', sa.Text, nullable=False)
    creation_thread_ts = sa.Column('creation_thread_ts', sa.Text, nullable=False, unique=True)
    draft_message_ts = sa.Column('draft_message_ts', sa.Text)
    creation_cursor = sa.Column('creation_cursor', sa.Text, default='blank')

    image_id = sa.Column('image_id', sa.Integer, sa.ForeignKey('images.id'))
    image = sa.orm.relationship('Image')

    description = sa.Column('description', sa.UnicodeText)

    rarity = sa.Column('rarity', sa.Integer)

    rarity_mapping = {
        500: RarityName.S,
        400: RarityName.A,
        300: RarityName.B,
        200: RarityName.C,
        100: RarityName.F,
    }
    rarity_values = {v: k for k, v in rarity_mapping.items()}

    def rarity_string(self) -> str:
        if self.rarity is None:
            return 'None'

        return str(self.rarity_mapping[self.rarity])

    def set_rarity(self, rarity: RarityName):
        self.rarity = self.rarity_values[rarity]

    hit_points = sa.Column('hit_points', sa.Integer)

    primary_nature = sa.Column('primary_nature', sa.UnicodeText)
    secondary_nature = sa.Column('secondary_nature', sa.UnicodeText)
    stupid = sa.Column('stupid', sa.Integer)
    baby = sa.Column('baby', sa.Integer)
    cursed = sa.Column('cursed', sa.Integer)
    horny = sa.Column('horny', sa.Integer)
    clown = sa.Column('clown', sa.Integer)
    feral = sa.Column('feral', sa.Integer)

    @staticmethod
    def sanitize_name(name: str) -> str:
        return ' '.join(name.strip().split())

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str]]:
        is_valid = True
        errors = []
        if len(name) > 140:
            errors.append('Must be under 140 characters.')

        has_non_ws_characters = re.compile(r"(?:\s*\S\s*){3,}")
        if not has_non_ws_characters.search(name):
            errors.append('Must have 3 or more characters.')

        errors = ' '.join(errors) if len(errors) else None

        return is_valid, errors

    @staticmethod
    def sluggify_name(name: str) -> str:
        # TODO: oof: using idna was a mistake, it's limited to 63 character chunks
        # this is gonna cause undefined behavior at the chunk boundaries with multibyte characters.
        # also good luck generating n-grams for search.
        parts = [
            ''.join([
                chunk.encode('idna').decode('utf-8')
                for chunk in re.findall(r'.{1,63}', part)
            ])
            for part in name.strip().split()
        ]
        return '-'.join(parts).lower()

    # todo: too complicated
    @staticmethod
    def rarity_prices() -> Dict[RarityName, int]:
        return {
            RarityName.S: 1000,
            RarityName.A: 403,
            RarityName.B: 181,
            RarityName.C: 81,
            RarityName.F: 7,
        }

    def price(self) -> int:
        return self.rarity_prices()[self.rarity_mapping[self.rarity]]

    def roll_stats(self):
        card = EngineCard.generate(self.name,
                                   self.rarity_mapping[self.rarity],
                                   [self.primary_nature, self.secondary_nature])
        # todo: smelly
        self.stupid = card.stupid
        self.baby = card.baby
        self.cursed = card.cursed
        self.horny = card.horny
        self.clown = card.clown
        self.feral = card.feral

    def set_name(self, name):
        name = self.sanitize_name(name)
        is_valid, error = self.validate_name(name)
        if error:
            raise InvalidCardName(error)

        self.name = name
        self.slug = self.sluggify_name(name)

    @property
    def is_complete(self) -> bool:
        required_attrs = [
            self.id,
            self.name,
            self.rarity,
            self.primary_nature,
            self.secondary_nature,
            self.stupid,
            self.baby,
            self.clown,
            self.horny,
            self.cursed,
            self.feral,
        ]
        for required_value in required_attrs:
            if not required_value:
                return False

        return True

    # TODO get rid of this optional return type somehow
    @property
    def engine(self) -> Optional[EngineCard]:

        # TODO: make this use self.is_complete
        required_attrs = [self.id, self.name, self.rarity, self.primary_nature, self.secondary_nature]
        for required_value in required_attrs:
            if not required_value:
                # returning none is a very dumb API
                return None

        maybe = {}

        if self.image and self.image.url:
            maybe['image_url'] = self.image.url

        # todo: this is sorta out of control
        return EngineCard(
            card_id=self.id,
            name=self.name,
            rarity=self.rarity_mapping[self.rarity],
            nature=(NatureName(self.primary_nature), NatureName(self.secondary_nature)),
            stupid=self.stupid,
            baby=self.baby,
            clown=self.clown,
            horny=self.horny,
            cursed=self.cursed,
            feral=self.feral,
            **maybe,
        )

    @classmethod
    def search_for(cls, session: Session, search: str) -> List[Card]:
        slug = cls.sluggify_name(search)
        return session.query(cls) \
            .filter(cls.published == True) \
            .filter(cls.slug.ilike(f'%{slug}%')) \
            .all()

    @classmethod
    def search_for_one(cls, session: Session, search: str) -> Optional[Card]:
        slug = cls.sluggify_name(search)

        results = cls.search_for(session, search)

        if not results:
            return None

        # return exact match if it exists
        for result in results:
            if result.slug == slug:
                return result

        # return shortest match
        results.sort(key=lambda card: len(card.slug))
        return results[0]

    def __repr__(self):
        return f"<Card(id='{self.id}', name='{self.name}' owner='{self.owner}')>"


_user_identity = Union[User, int]


def get_game_cards(session: Session,
                   user: _user_identity = None,
                   user_slack_id: str = None) -> List[GameCard]:
    cards = session.query(Card).join(User).filter(Card.published == True)

    if user:
        if isinstance(user, User):
            cards = cards.filter(User.id == user.id)
        elif isinstance(user, int):
            cards = cards.filter(User.id == user)
        else:
            raise ValueError("Don't know how to handle this user param")
    elif user_slack_id:
        cards = cards.filter(User.slack_id == user_slack_id)

    cards = cards.all()

    if not cards:
        return []

    return [card.engine for card in cards if card.engine]
