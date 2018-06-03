from os import environ

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from urls import map_urls
from models import session


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


def init_sqlalchemy(app):
    """Initialize SQLAlchemy and hook automocommit.

    Arguments:
    app -- the app to hook SQLAlchemy
    """

    @app.after_request
    def after_request(response):
        session.commit()
        return response

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@db/hermes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    app.db = db
    app.flask_session = app.db.session

    # migrations
    Migrate(app, db)

    return db


init_sqlalchemy(app)
map_urls(app)

if __name__ == '__main__':
    app.logger.info('Hermes speed')
    app.run(host="0.0.0.0", debug=True)
