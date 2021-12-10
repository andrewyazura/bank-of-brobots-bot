from config import Config
from flask import Flask
from flask_marshmallow import Marshmallow

from brobank_bot.telegram_bot import TelegramBot

telegram_bot = TelegramBot()
marshmallow = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    telegram_bot.init_app(app)
    marshmallow.init_app(app)

    with app.app_context():
        from brobank_bot.routes import routes_bp

        app.register_blueprint(
            routes_bp, url_prefix=f"/{app.config.get('TELEGRAM_BOT', {}).get('TOKEN')}"
        )

    return app
