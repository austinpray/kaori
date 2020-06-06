import re
from typing import Tuple, Optional, Dict

import sqlalchemy as sa
import sqlalchemy.orm

from kaori.support.models.Models import Base


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

    def rarity_string(self) -> str:
        if self.rarity is None:
            return 'None'

        return [
            'S',
            'A',
            'B',
            'C',
            'F',
        ][self.rarity]

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
        return '-'.join(name.strip().split()).lower().encode('idna').decode('utf-8')

    @staticmethod
    def rarity_prices() -> Dict[str, int]:
        return {
            'SS': 2000,
            'S': 1000,
            'A': 403,
            'B': 181,
            'C': 81,
            'D': 36,
            'E': 16,
            'F': 7,
        }

    def set_name(self, name):
        name = self.sanitize_name(name)
        is_valid, error = self.validate_name(name)
        if error:
            raise InvalidCardName(error)

        self.name = name
        self.slug = self.sluggify_name(name)

    def __repr__(self):
        return f"<Card(id='{self.id}', name='{self.name}' owner='{self.owner}')>"
