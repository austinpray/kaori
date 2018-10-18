import itertools
from random import choice
import re

import sqlalchemy.orm as orm
from slacktools.message import format_url

from config import KIZUNA_WEB_URL

from kizuna.adapters.slack import SlackAdapter, SlackCommand, SlackMessage
from kizuna.skills.db import DB
from kizuna.support.utils import build_url
from .models import ReactionImageTag
from kizuna.plugins.users.models import User


no_user_message = "I don't have your users in the db. Prolly run 'kizuna refresh users' and if that still doesn't fix" \
                  "it: Austin fucked up somewhere :^("

def authenticated_path(user, path):
    return build_url(KIZUNA_WEB_URL, path, {'auth': user.get_token()})


class AddReactionCommand(SlackMessage):
    """usage: {bot} react add - add a new reaction image to the collection"""

    @staticmethod
    def handle(message: SlackMessage, bot: SlackAdapter, db: DB):
        pattern = re.compile('react(?:ion) add', re.IGNORECASE)
        if not bot.addressed_by(message) or not bot.understands(message, with_pattern=pattern):
            return

        with db.session_scope() as session:
            user = User.get_by_slack_id(session, message.user)

            if not user:
                return bot.reply(message, no_user_message, ephemeral=True)

            react_add_image_url = authenticated_path(user, '/react/images/new')

            return bot.reply(message, react_add_image_url, ephemeral=True)


class ReactCommand(SlackCommand):
    """usage: {bot} tfw QUERY... - fetch a reaction image for the query"""

    @staticmethod
    def respond(message: SlackMessage, bot: SlackAdapter, db: DB):
        if not bot.addressed_by(message):
            return

        matches = bot.understands(message, with_pattern=re.compile('tfw (.*)', re.IGNORECASE))

        if not matches:
            return

        query = matches.group(1).strip()

        with db.session_scope() as session:

            user = User.get_by_slack_id(session, message.user)

            if not user:
                return bot.reply(message, no_user_message, ephemeral=True)

            react_homepage_url = authenticated_path(user, '/react')
            react_add_image_url = authenticated_path(user, '/react/images/new')

            # kizuna react <tag>
            def add_images_nag():
                add_images = format_url('(Add Images)', react_add_image_url)
                view_images = format_url('(View Images)', react_homepage_url)
                bot.reply(message, f"You can add some images though! {add_images} {view_images}", ephemeral=True)

            possible_tags = [token.strip().lower() for token in query.split()]

            tags = (session
                    .query(ReactionImageTag)
                    .options(orm.joinedload("images"))
                    .filter(ReactionImageTag.name.in_(possible_tags))
                    .all())

            if tags:
                images = list(itertools.chain.from_iterable([tag.images for tag in tags]))

                if len(images) > 0:
                    for image in images:
                        image.tags_text = [tag.name for tag in image.tags if tag.name in possible_tags]
                    images.sort(key=lambda t: len(t.tags_text), reverse=True)
                    best_match_length = len(images[0].tags_text)
                    best_matches = [image for image in images if len(image.tags_text) == best_match_length]
                    return bot.respond(message, choice(best_matches).url)

                return [
                    bot.respond(message, f"I don't have any images for \"{query}\" :^("),
                    add_images_nag()
                ]

            return [
                bot.respond(message, f"I don't have anything for \"{query}\" :^("),
                add_images_nag()
            ]
