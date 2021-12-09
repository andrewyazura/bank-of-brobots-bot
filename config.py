import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    TELEGRAM_BOT = dict(
        TOKEN=os.environ.get("TELEGRAM_BOT_TOKEN"),
        DOMAIN=os.environ.get("TELEGRAM_BOT_DOMAIN"),
        CERTIFICATE=os.environ.get("TELEGRAM_BOT_CERTIFICATE"),
    )
    API_URL = os.environ.get("API_URL")
