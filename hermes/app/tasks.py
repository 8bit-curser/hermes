from os import environ

from celery import Celery

app = Celery('tasks', broker=environ.get('CELERY_BROKER'))
app.conf.result_backend = environ.get('CELERY_BACKEND')


@app.task
def test_task():
    print("hello")
