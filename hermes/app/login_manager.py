from datetime import timedelta

from flask import g, redirect, request, session, url_for
from flask_login import LoginManager, current_user

from models import User


def init_login_manager(app):
    """Initialize the login manager.init_app

    Arguments:
    app -- hooks the login_manager to the app.
    """
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(email):
        return User.query.filter_by(email=email).first()

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        next_url = request.endpoint
        return redirect(url_for("login", next_url=next_url))

    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=2)
        session.modified = True
        g.user = current_user

    return login_manager
