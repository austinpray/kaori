import re
from typing import Tuple, Optional, Dict

import sqlalchemy as sa
import sqlalchemy.orm

from kaori.support.models.Models import Base
from ..engine.core import RarityName, Card as EngineCard, NatureName


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
        # oof: using idna was a mistake, it's limited to 63 character chunks
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

    # TODO get rid of this optional return type somehow
    @property
    def engine(self) -> Optional[EngineCard]:
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

    def __repr__(self):
        return f"<Card(id='{self.id}', name='{self.name}' owner='{self.owner}')>"
