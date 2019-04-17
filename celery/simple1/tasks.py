from celery import Celery

app = Celery('tasks', broker = 'pyamqp://guest@localhost//')

@app.task
def add(x, y):
    z = x + y
    return (z)