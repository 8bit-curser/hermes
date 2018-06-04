from celery import Celery

app = Celery('tasks', broker="pyamqp://guest@rabbitmq/")
app.conf.result_backend = "db+postgresql://postgres@db/celery"


