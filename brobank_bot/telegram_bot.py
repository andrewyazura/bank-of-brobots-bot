import logging
from functools import wraps
from queue import Queue

from flask import request
from telegram import Update
from telegram.ext import Defaults, Dispatcher, ExtBot, JobQueue
from telegram.utils.request import Request


class TelegramBot(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.config = app.config.get("TELEGRAM_BOT")
        self.logger = logging.getLogger("telegram_bot")

        token = self.config.get("TOKEN")
        workers = int(self.config.get("WORKERS")) if app.debug else 0
        con_pool_size = workers + 4
        update_queue = Queue() if app.debug else None
        job_queue = JobQueue() if app.debug else None
        defaults = Defaults(**self.config.get("DEFAULTS"))

        request = Request(con_pool_size=con_pool_size)
        self.bot = ExtBot(token, request=request)
        self.dispatcher = Dispatcher(
            bot=self.bot,
            workers=workers,
            update_queue=update_queue,
            job_queue=job_queue,
            defaults=defaults,
        )

        self.app = app
        app.telegram_bot = self.bot
        app.dispatcher = self.dispatcher

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
