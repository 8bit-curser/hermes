from os import environ

from celery import Celery
from celery.task.control import inspect
from flask_mail import Mail, Message

from hermes.app.app import app as flask_app
from hermes.app.enums import RequestStateEnum
from hermes.app.models import Item, Request, session

app = Celery('tasks', broker=environ.get('CELERY_BROKER'))
app.conf.result_backend = environ.get('CELERY_BACKEND')


@app.task
def mail_send(msg):
    """Generates example email.i
    Arguments:
        msg -- string of the message sent
    """
    # This shall be replaced with a proper email fowarding function, in order
    # to achieve that another docker must be deployed and connected to this one
    # creating a 'Swarm'
    return msg


@app.task
def update_reqs(item_id):
    """After restocking update all requests as done.
    Arguments:
        item_id -- Item class registry id
    """
    reqs = Request.query.filter(Request.item_id == item_id,
                                Request.state == RequestStateEnum.sent).all()
    for req in reqs:
        req.state = RequestStateEnum.done
        session.commit()


@app.task
def update_item_after_restock(item_id):
    """After requests have been updated the amounts should be substracted.
    Arguments:
        reqs -- collection of requests
    """
    reqs = Request.query.filter(Request.item_id == item_id,
                                Request.state == RequestStateEnum.sent).all()

    total_amounts = sum([req.amount for req in reqs])
    item = Item.query.get(item_id)
    item.amount = total_amounts - item.amount
    session.commit()

    update_reqs.delay(item_id)



