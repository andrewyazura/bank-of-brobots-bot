from logging.config import dictConfig

from flask import Flask
from flask_marshmallow import Marshmallow

from brobank_bot.telegram_bot import TelegramBot
from config import Config

telegram_bot = TelegramBot()
marshmallow = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    dictConfig(config_class.LOG_CONFIG)

    telegram_bot.init_app(app)
    marshmallow.init_app(app)

    with app.app_context():
        import brobank_bot.handlers  # noqa: F401
        from brobank_bot.routes import routes_bp

        app.register_blueprint(
            routes_bp, url_prefix=f"/{app.config.get('TELEGRAM_BOT', {}).get('TOKEN')}"
        )

    return app
