import copy
import re
from typing import Tuple, List, Optional, Union
from uuid import uuid4

from slacktools.message import extract_mentions
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from kaori.adapters.slack import SlackCommand, SlackMessage, SlackAdapter
from kaori.plugins.users import User, UserNotFound
from kaori.skills import DB, FileUploader
from ..engine.core import RarityName, NatureName
from ..models.Card import InvalidCardName, Card
from ..models.Image import Image
from ..tui import render_card, instructions_blocks, query_rarity_blocks, query_nature_blocks
from ..utils import tmp_prefix


class CreateCardCommand(SlackCommand):
    """usage: {bot} create card - start card creation"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB, file_uploader: FileUploader):
        if not bot.addressed_by(message):
            return

        # start a conversation
        if not bot.understands(message, with_pattern=re.compile(r'create\s+card|card\s+create$', re.I)):
            return

        if message.is_thread_reply:
            return

        try:
            with db.session_scope() as session:
                user = User.get_by_slack_id(session, message.user)

                if not user:
                    raise UserNotFound('cannot find user')

                # allow creation to recover from errors
                card = resume_card(session,
                                   thread_ts=message.thread_ts,
                                   user=message.user)

                if not card:
                    card = initialize_card(message, user)

                    session.add(card)
                    session.commit()

                bot.reply(message,
                          blocks=instructions_blocks(bot_name=bot.mention_string),
                          create_thread=True)

                draft_message = bot.reply(message,
                                          **render_card(card=card),
                                          create_thread=True,
                                          reply_broadcast=True)

                if not draft_message.get('ok'):
                    print(draft_message)
                    return

                card.draft_message_ts = draft_message.get('ts')
                session.merge(card)

        except UserNotFound as e:
            bot.reply(message, "Something is wrong...cannot find your user. Try 'kaori refresh users'")
            return

        # fake thread
        # todo: this is kinda dumb
        message = copy.deepcopy(message)
        message.is_thread = True
        message.thread_ts = message.ts

        await UpdateCardCommand.handle(message=message, bot=bot, db=db, file_uploader=file_uploader)


class UpdateCardCommand(SlackCommand):
    """usage: {bot} update card properties"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB, file_uploader: FileUploader):
        if not bot.addressed_by(message) or not message.is_thread:
            return

        try:
            session: Session
            with db.session_scope() as session:
                card = resume_card(session,
                                   thread_ts=message.thread_ts,
                                   user=message.user)

                # this thread is not related to a card creation, ignore
                if not card:
                    return

                # lol god this is quickly getting away from me
                # just let me finish this and I'll refactor later
                user_input = ''

                catch_all_pattern = re.compile(r'(.*)', re.IGNORECASE)
                matches = bot.understands(message, with_pattern=catch_all_pattern)

                if not matches:
                    return

                user_input = matches[1].strip()

                if user_input == 'refresh preview':
                    refresh_card_preview(card, bot)
                    return

                if card.creation_cursor == 'set_image':
                    if message.files:
                        img = Image.from_slack_message(message=message,
                                                       session=session,
                                                       slack_adapter=bot,
                                                       uploader=file_uploader)
                        card.image = img
                        card.creation_cursor = 'query_description'
                        bot.react(message, 'thumbsup')
                    else:
                        bot.reply(message, 'upload an image to slack')
                        return

                card, replies = next_card_creation_step(card=card,
                                                        user_input=user_input,
                                                        session=session)

                refresh_card_preview(card, bot)

                session.merge(card)
                session.commit()

                for reply in replies:
                    if reply == ':+1:':
                        bot.react(message, 'thumbsup')
                    else:
                        if isinstance(reply, dict):
                            bot.reply(message, create_thread=True, **reply)
                        else:
                            bot.reply(message, reply, create_thread=True)

        except InvalidCardName as e:
            bot.reply(message, str(e))
        except IntegrityError as e:
            bot.reply(message,
                      f"Something is wrong with that input...try again or ask Austin to fix it. Code {e.code}")
            print(e)


def refresh_card_preview(card: Card, bot: SlackAdapter):
    res = bot.edit(
        SlackMessage({
            'event': {
                'ts': card.draft_message_ts,
                'channel': card.creation_thread_channel
            }
        }),
        **render_card(card)
    )
    if not res['ok']:
        print(res)


def initialize_card(message: SlackMessage, user: User) -> Card:
    tmp_name = tmp_prefix + str(uuid4())
    card = Card(name=tmp_name,
                slug=tmp_name,
                owner=user.id,
                creation_cursor='blank',
                published=False,
                creation_thread_channel=message.channel,
                creation_thread_ts=message.ts)

    return card


# This is essentially a state machine.
# Right now this is spaghetti code for prototyping purposes.
# TODO: Once the functionality is totally built out we can break this into multiple functions etc.
# BODY: Oh god break this into some functions please, this should be a dispatcher or something.
# This function is now officially out of control
def next_card_creation_step(card: Card,
                            session: Session,
                            user_input: str) -> Tuple[Card, List[Union[str, dict]]]:
    replies = []

    if user_input == 'quit':
        replies.append('Got it. I will delete this card :+1:. See you next time!')
        card.creation_cursor = 'deleted'
        return card, replies

    cursor = card.creation_cursor

    if cursor == 'blank' or user_input == 'create card' or user_input == 'start over':
        cursor = 'query_name'

    if cursor.startswith('set_'):
        if len(extract_mentions(user_input)):
            replies.append('Mentions are not allowed in gacha card text')
            return card, replies

        if cursor == 'set_name':
            card.set_name(user_input)

            num_dupes = session \
                .query(Card) \
                .filter(Card.id != card.id) \
                .filter(Card.slug == card.slug) \
                .count()

            if num_dupes > 0:
                raise InvalidCardName('That name is taken')

            replies.append(':+1:')
            cursor = 'query_image'
        elif cursor == 'set_description':
            card.description = user_input
            replies.append(':+1:')
            cursor = 'query_nature'
        elif cursor == 'set_nature':
            nature_patterns = NatureName.to_regex()
            matches = re.search(f'({nature_patterns}).+?({nature_patterns})',
                                user_input,
                                re.I)
            if matches:
                primary_nature, secondary_nature = matches.group(1, 2)
                if primary_nature == secondary_nature:
                    replies.append('You have to choose two different natures.')
                else:
                    card.primary_nature = primary_nature.lower()
                    card.secondary_nature = secondary_nature.lower()
                    replies.append(':+1:')
                    cursor = 'query_rarity'
            else:
                replies.append('You need to specify some natures.')

        elif cursor == 'set_rarity':
            pattern = f'({RarityName.to_regex()})(?:-tier)?'
            match = None
            for token in user_input.split():
                match = re.match(pattern, token)
                if match:
                    card.set_rarity(RarityName(match.group(1)))
                    replies.append(':+1:')
                    cursor = 'do_stats_roll'
            if not match:
                replies.append('Need to specify a rarity')
        elif cursor == 'set_confirm_price':
            # todo: make utility for capturing english affirmatives
            if re.search(r'yes+|yep+|ye+|yeah+', user_input, re.IGNORECASE):
                card.published = True
                cursor = 'done'
            # todo: make utility for capturing english negatives
            elif re.search(r'no+|nope+|', user_input, re.IGNORECASE):
                replies.append("Okay. If you change your mind:\n"
                               "• Reply with `@kaori yes` to accept the card\n"
                               "• Reply with `@kaori start over` to trash your current card")
            else:
                replies.append("I don't understand: yes or no?")

    if cursor == 'do_stats_roll':
        card.roll_stats()
        cursor = 'query_confirm_price'

    if cursor.startswith('query_'):
        if cursor == 'query_name':
            replies.append('*What would you like name the card?*')
            cursor = 'set_name'
        elif cursor == 'query_image':
            replies.append(f'*Upload an image for {card.name}*')
            cursor = 'set_image'
        elif cursor == 'query_description':
            replies.append(f'*Description for {card.name}?*')
            cursor = 'set_description'
        elif cursor == 'query_nature':
            replies.append({'blocks': query_nature_blocks()})
            cursor = 'set_nature'
        elif cursor == 'query_rarity':
            replies.append({'blocks': query_rarity_blocks()})
            cursor = 'set_rarity'
        elif cursor == 'query_confirm_price':
            replies.append({'blocks': [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"This card will cost {card.price()}\n"
                                "*Are you sure* you want to create this card?"
                    },
                },
                *render_card(card)['blocks']
            ]})
            cursor = 'set_confirm_price'

    if cursor == 'done':
        replies.append('*Congrats!* Your card is created. Enjoy.')

    card.creation_cursor = cursor
    return card, replies


def resume_card(session, thread_ts, user) -> Optional[Card]:
    return session \
        .query(Card) \
        .join(User) \
        .filter(Card.creation_thread_ts == thread_ts) \
        .filter(Card.published == False) \
        .filter(User.slack_id == user) \
        .first()
