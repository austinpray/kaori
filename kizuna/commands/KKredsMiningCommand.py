import arrow

from kizuna.Kizuna import Kizuna
from kizuna.commands import BaseCommand
from kizuna.kkreds import is_payable
from kizuna.kkreds import strip_date
from kizuna.models import User, KKredsTransaction
from kizuna.slack import reply


class KKredsMiningCommand(BaseCommand):
    def __init__(self, make_session, kizuna: Kizuna) -> None:
        self.kizuna = kizuna

        help_text = 'kizuna pay me - at 4:20 in the America/Chicago time zone on both meridians you can say "pay me" ' \
                    'and you will be awarded a kkred '

        triggers = [
            ".*(?:gibbe|give) money.*",
            ".*pay me.*",
            ".*:watermelon:.*"
        ]

        pattern = "|".join(triggers)
        super().__init__(name='mine_kkred',
                         pattern=pattern,
                         help_text=help_text,
                         is_at=False,
                         db_session_maker=make_session)

    def respond(self, slack_client, message, matches):
        message_ts = arrow.get(message['event_ts'])

        if not is_payable(message_ts):
            return

        user_id = message['user']

        with self.db_session_scope() as session:
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

            kizuna_user = User.get_by_slack_id(session, self.kizuna.bot_id)
            mined_kkred = KKredsTransaction(from_user=kizuna_user,
                                            to_user=user,
                                            amount=1,
                                            is_mined=True,
                                            created_at=message_ts.datetime)

            session.add(mined_kkred)

        reply(slack_client, message, 'successfully mined 1 kkred')
