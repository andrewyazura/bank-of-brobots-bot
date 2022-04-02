from telegram.ext import CommandHandler

from brobank_bot import telegram_bot


@telegram_bot.register_handler(CommandHandler, "start")
def start(update, context):
    user = update.effective_user
    user.send_message("Hey there!")
