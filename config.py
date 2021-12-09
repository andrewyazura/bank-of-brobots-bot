import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


def get_env_group(prefix):
    return {k[len(prefix) :]: v for k, v in os.environ.items() if k.startswith(prefix)}


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    API_URL = os.environ.get("API_URL")

    TELEGRAM_BOT = get_env_group("TELEGRAM_BOT_")
