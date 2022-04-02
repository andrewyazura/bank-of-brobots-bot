from flask import Blueprint

from brobank_bot import telegram_bot

webhook_bp = Blueprint("webhook", __name__, url_prefix="/webhook")


@webhook_bp.route("", methods=["POST"])
@telegram_bot.parse_telegram_update
def webhook(update):
    telegram_bot.dispatcher.process_update(update)
