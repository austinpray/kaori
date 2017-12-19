from kizuna.commands.Command import Command
from kizuna.models.User import User
from kizuna.models.KKredsTransaction import KKredsTransaction
from datetime import datetime
from kizuna.kkreds import strip_date

from kizuna.kkreds import is_payable
import arrow
from kazoo.client import KazooClient
from kizuna.Kizuna import Kizuna


class KKredsMiningCommand(Command):
    def __init__(self, make_session, kizuna: Kizuna, zk: KazooClient) -> None:
        self.make_session = make_session
        self.zk = zk
        self.kizuna = kizuna

        help_text = 'kizuna pay me - at 4:20 in the America/Chicago time zone on both meridians you can say "pay me" ' \
                    'and you will be awarded a kkred '

        triggers = [
            ".*(?:gibbe|give) money.*",
            ".*pay me.*",
            ".*:watermelon:.*"
        ]

        pattern = "|".join(triggers)
        super().__init__('ping$', pattern, help_text, is_at=False, always=True)

    def respond(self, slack_client, message, matches):
        message_ts = arrow.get(message['event_ts'])

        if not is_payable(message_ts):
            return

        session = self.make_session()

        user_id = message['user']

        user = User.get_by_slack_id(session, user_id)
        if not user:
            return

        lock = self.zk.Lock('/lockpath', f'kkred-mine-{user_id}')

        lock.acquire(blocking=True, timeout=10)

        try:
            latest_mine = session\
                .query(KKredsTransaction)\
                .filter(KKredsTransaction.to_user_id == user.id)\
                .filter(KKredsTransaction.is_mined)\
                .order_by(KKredsTransaction.created_at.desc())\
                .first()

            if latest_mine and latest_mine.created_at:
                message_ts_stripped = strip_date(message_ts)
                latest_mine_time_stripped = strip_date(latest_mine.created_at)
                if latest_mine_time_stripped >= message_ts_stripped:
                    self.reply(slack_client, message, 'not payable')
                    lock.release()
                    return

            kizuna_user = User.get_by_slack_id(session, self.kizuna.bot_id)
            mined_kkred = KKredsTransaction(from_user=kizuna_user,
                                            to_user=user,
                                            amount=1,
                                            is_mined=True,
                                            created_at=message_ts.datetime)

            session.add(mined_kkred)
            session.commit()

            self.reply(slack_client, message, 'payable')
        finally:
            lock.release()
