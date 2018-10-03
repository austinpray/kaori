import importlib.util
import os

from flask import Flask
from raven.contrib.flask import Sentry

from .views import blueprint as views_blueprint

spec = importlib.util.spec_from_file_location("config.kizuna", os.path.join(os.getcwd(), 'config/kizuna.py'))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

# DEV_INFO = Kizuna.read_dev_info('./.dev-info.json')

app = Flask(__name__, static_folder=config.STATIC_DIR)

app.secret_key = config.SECRET_KEY

app.config['SENTRY_CONFIG'] = {
    'dsn': config.SENTRY_URL,
    # 'release': DEV_INFO.get('revision'),
    'environment': config.KIZUNA_ENV
}

sentry = Sentry(app) if config.SENTRY_URL else None

app.register_blueprint(views_blueprint)
