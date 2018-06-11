from os import environ

from celery import Celery
from celery.task.control import inspect
from flask_mail import Mail, Message

from hermes.app.app import app as flask_app
from hermes.app.enums import RequestStateEnum
from hermes.app.models import Request

app = Celery('tasks', broker=environ.get('CELERY_BROKER'))
app.conf.result_backend = environ.get('CELERY_BACKEND')


@app.task
def mail_send(msg):
    """Generates example email."""
    #  msg = Message("Test",
                  #  sender="example@mail.com",
                  #  recipients=["example2@mail.com"])
        # In order to do this we have to mount a docker
        # mail server hook it to the same network as this one
        # and then set it up to use it.
        #  mail = Mail(flask_app)
    return msg
        #  mail.send(msg)


#  @app.task
#  def push_request():
    #  reqs = Request.query.filter(
        #  Request.state == RequestStateEnum.ready).sort_by(Request.timestamp)

    #  for req in reqs:

