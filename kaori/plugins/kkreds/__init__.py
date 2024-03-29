import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from random import randint

import arrow
from arrow import Arrow
from kaori.support.slacktools.message import is_user_mention, extract_user_id_from_mention
from sqlalchemy import func

from kaori.adapters.slack import SlackAdapter, SlackMessage, SlackCommand
from kaori.plugins.users import User
from kaori.skills.db import DB
from .models import KKredsTransaction


def get_kkred_balance(user: User, session) -> Decimal:
    kkred_debits = session \
        .query(func.sum(KKredsTransaction.amount)) \
        .filter(KKredsTransaction.from_user_id == user.id) \
        .first()[0]

    if kkred_debits is None:
        kkred_debits = Decimal(0)

    kkred_credits = session \
        .query(func.sum(KKredsTransaction.amount)) \
        .filter(KKredsTransaction.to_user_id == user.id) \
        .first()[0]

    if kkred_credits is None:
        kkred_credits = Decimal(0)

    return kkred_credits - kkred_debits


def is_payable(utc: Arrow) -> bool:
    """Should return True if time is 4:20AM or 4:20PM in Texas"""

    central = utc.to('America/Chicago')

    hour = central.hour
    minute = central.minute

    if minute != 20:
        return False

    if hour not in [4, 16]:
        return False

    return True


# 2020: https://github.com/austinpray/kaori/commit/232c01ffee9c8013ae845e4cc19c2018ea2b40c6
# 2021:
# 2022:
def should_mega_pay(utc: Arrow) -> bool:
    """Should return True it is 4/20/2022 4:20 AM/PM in Texas"""

    central = utc.to('America/Chicago')

    return (central.month == 4 and
            central.day == 20 and
            central.year == 2022 and
            is_payable(utc))

def mega_pay_amount(seconds: int, microseconds: int) -> int:
    x = (seconds+(microseconds*1e-6))/60
    return round(4200-((79800*x)/(1+18*abs(x))))


def strip_date(target_date):
    return arrow.get(datetime(year=target_date.year,
                              month=target_date.month,
                              day=target_date.day,
                              hour=target_date.hour,
                              minute=target_date.minute))


class KKredsBalanceCommand(SlackCommand):
    """{bot} balance - show your kkreds balance"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB):
        pattern = re.compile('balance', re.IGNORECASE)

        if not bot.addressed_by(message) or not bot.understands(message, with_pattern=pattern):
            return

        with db.session_scope() as session:
            user = User.get_by_slack_id(session, message.user)
            balance = get_kkred_balance(user, session)

        pluralized_kkreds = 'kkred' if balance == 1 else 'kkreds'
        return bot.reply(message, f'your balance is {balance} {pluralized_kkreds}')


class KKredsMiningCommand(SlackCommand):
    """
    {bot} pay me - at 4:20 in the America/Chicago time zone on both meridians you can say "pay me" and you will be
    awarded a kkred
    """

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB):

        pattern = "|".join([
            ".*(?:gibbe|give) money.*",
            ".*pay me.*",
            ".*:watermelon:.*"
        ])

        trigger = re.compile(pattern, re.IGNORECASE)

        message_ts = arrow.get(message.ts, 'X')

        if not is_payable(message_ts) or not bot.understands(message, with_pattern=trigger):
            return

        user_id = message.user

        with db.session_scope() as session:
            user = User.get_by_slack_id(session, user_id)

            if not user:
                return

            latest_mine = session \
                .query(KKredsTransaction) \
                .filter(KKredsTransaction.to_user_id == user.id) \
                .filter(KKredsTransaction.is_mined) \
                .order_by(KKredsTransaction.created_at.desc()) \
                .first()

            if latest_mine and latest_mine.created_at:
                message_ts_stripped = strip_date(message_ts)
                latest_mine_time_stripped = strip_date(latest_mine.created_at)
                if latest_mine_time_stripped >= message_ts_stripped:
                    return

            amount = 1

            if should_mega_pay(message_ts):
                amount = mega_pay_amount(message_ts.second, message_ts.microsecond)

            kaori_user = User.get_by_slack_id(session, bot.id)
            mined_kkred = KKredsTransaction(from_user=kaori_user,
                                            to_user=user,
                                            amount=amount,
                                            is_mined=True,
                                            created_at=message_ts.datetime)

            session.add(mined_kkred)

        pluralized = '1 kkred' if amount == 1 else f'{amount} kkreds'
        bot.reply(message, f'successfully mined {pluralized}')


class KKredsTransactionCommand(SlackCommand):
    """{bot} pay <user> <amount> - pay the user that amount of kkreds"""

    @staticmethod
    async def handle(message: SlackMessage, bot: SlackAdapter, db: DB):

        pattern = re.compile(r'(?:pay|tip|give|send)\s+(\S*)\s+(\S*)', re.IGNORECASE)

        if not bot.addressed_by(message):
            return

        matches = bot.understands(message, with_pattern=pattern)

        if not matches:
            return

        message_ts = arrow.get(message.ts, 'X')

        sending_user_id = message.user

        with db.session_scope() as session:
            sending_user = User.get_by_slack_id(session, sending_user_id)

            if not sending_user:
                return

            receiving_user_raw = matches[1]

            if not is_user_mention(receiving_user_raw):
                return bot.reply(message,
                                 'User has to be an `@` mention. Like it has to be a real blue `@` mention.')

            receiving_user = User.get_by_slack_id(session,
                                                  extract_user_id_from_mention(receiving_user_raw))

            if not receiving_user:
                return bot.reply(message, 'Could not find that user')

            if sending_user.id == receiving_user.id:
                return bot.reply(message,
                                 'You can’t send money to yourself.')

            amount_raw = matches[2]

            try:
                amount = Decimal(amount_raw)
            except InvalidOperation:
                return bot.reply(message,
                                 'That amount is invalid. Try a decimal or integer value')

            if amount <= 0:
                return bot.reply(message,
                                 'Amount has to be non-zero')

            if amount > get_kkred_balance(sending_user, session):
                return bot.reply(message,
                                 'You don’t have enough kkreds')

            transaction = KKredsTransaction(from_user=sending_user,
                                            to_user=receiving_user,
                                            amount=amount,
                                            created_at=message_ts.datetime)

            session.add(transaction)

            bot.reply(message, f'successfully sent {amount} to {receiving_user.name}')
