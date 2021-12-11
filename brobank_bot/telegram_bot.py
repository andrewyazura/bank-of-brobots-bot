from functools import wraps
from queue import Queue

from flask import request
from telegram import Update
from telegram.ext import Dispatcher, ExtBot, JobQueue
from telegram.utils.request import Request


class TelegramBot(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        bot_config = app.config.get("TELEGRAM_BOT")

        token = bot_config.get("TOKEN")
        workers = int(bot_config.get("WORKERS")) if app.debug else 0
        con_pool_size = workers + 4
        update_queue = Queue() if app.debug else None
        job_queue = JobQueue() if app.debug else None

        request = Request(con_pool_size=con_pool_size)
        self.bot = ExtBot(token, request=request)
        self.dispatcher = Dispatcher(
            bot=self.bot,
            workers=workers,
            update_queue=update_queue,
            job_queue=job_queue,
        )

        if not app.debug:
            self.set_webhook(app)

        self.app = app
        app.telegram_bot = self.bot
        app.dispatcher = self.dispatcher

    def set_webhook(self, app):
        bot_config = app.config.get("TELEGRAM_BOT")
        domain = bot_config.get("DOMAIN")
        token = bot_config.get("TOKEN")
        cert_path = bot_config.get("CERTIFICATE")

        url = f"{domain}/{token}/webhook"
        self.bot.set_webhook(url=url, certificate=open(cert_path, "rb"))

    def parse_telegram_update(self, f):
        @wraps(f)
        def decorated_function(*_args, **_kwargs):
            parsed_update = Update.de_json(request.get_json(), self.bot)
            return f(parsed_update, *_args, **_kwargs)

        return decorated_function

    def register_handler(self, handler_class, *args, **kwargs):
        def decorator(f):
            handler = handler_class(*args, **kwargs, callback=f)
            self.dispatcher.add_handler(handler)
            return f

        return decorator
