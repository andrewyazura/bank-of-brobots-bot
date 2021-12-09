from flask import Blueprint

routes_bp = Blueprint("routes", __name__)

from brobank_bot.routes import telegram_bot
