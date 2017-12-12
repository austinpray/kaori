from . import KIZUNA_ENV

if KIZUNA_ENV == 'development':
    bind = '0.0.0.0:8000'

workers = 4
