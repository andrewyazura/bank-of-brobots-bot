import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"), override=True)


def get_env_group(prefix):
    return {k[len(prefix) :]: v for k, v in os.environ.items() if k.startswith(prefix)}


LOG_CONFIG = get_env_group("LOG_")


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    API_URL = os.environ.get("API_URL")

    TELEGRAM_BOT = get_env_group("TELEGRAM_BOT_")

    LOG_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "file": {
                "format": LOG_CONFIG.get("FORMAT"),
                "datefmt": LOG_CONFIG.get("DATEFMT"),
            }
        },
        "handlers": {
            "file": {
                "level": LOG_CONFIG.get("LEVEL"),
                "formatter": "file",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": LOG_CONFIG.get("FILENAME"),
                "when": "midnight",
                "backupCount": int(LOG_CONFIG.get("BACKUP_COUNT")),
                "utc": True,
            }
        },
        "loggers": {
            "telegram_bot": {"level": LOG_CONFIG.get("LEVEL"), "handlers": ["file"]}
        },
        "root": {"level": LOG_CONFIG.get("LEVEL"), "handlers": ["file"]},
    }
