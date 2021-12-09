from brobank_bot import telegram_bot
from brobank_bot.routes import routes_bp


@routes_bp.route("/webhook", methods=["POST"])
@telegram_bot.parse_telegram_update
def webhook(update):
    telegram_bot.dispatcher.process_update(update)
