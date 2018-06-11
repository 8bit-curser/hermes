from os import environ

from celery import Celery
from flask_mail import Mail, Message

from hermes.app.app import app as flask_app

app = Celery('tasks', broker=environ.get('CELERY_BROKER'))
app.conf.result_backend = environ.get('CELERY_BACKEND')


@app.task
def mail_send():
    """Generates example email."""
    msg = Message("Test",
                  sender="example@mail.com",
                  recipients=["example2@mail.com"])
    with flask_app.app_context():
        # In order to do this we have to mount a docker
        # mail server hook it to the same network as this one
        # and then set it up to use it.
        #  mail = Mail(flask_app)
        flask_app.logger.info(msg.__dict__)
        #  mail.send(msg)
