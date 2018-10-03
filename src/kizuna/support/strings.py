# coding=utf-8
import random

HAI_DOMO = 'はいども！キズナです！'
KIZUNA = 'キズナ'
WAIT_A_SEC = 'ちょっと待ってください'
JAP_DOT = '。'

AHO = 'あほ'
BAKA = 'ばか'
INSULTS = [AHO, BAKA]


def random_insult():
    return random.choice(INSULTS)


YOSHI = 'よし'

VERSION_UPDATE_TEMPLATE = '私は{{VERSION}}に更新しました'
VERSION_TRANSITION_TEMPLATE = '{{FROM_VERSION}}から{{TO_VERSION}}にバージョンアップしました。'

LQUO = '「'
RQUO = '」'

VERSION_UP = 'バージョンアップ'

GOODBYE = 'さよなら'
