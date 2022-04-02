from flask import Blueprint, current_app, request

from brobank_bot.routes.webhook import webhook_bp

routes_bp = Blueprint("routes", __name__)

routes_bp.register_blueprint(webhook_bp)


@routes_bp.before_request
def log_request_info():
    current_app.logger.info(
        f"{request.remote_addr} - {request.method} - {request.path}"
    )
