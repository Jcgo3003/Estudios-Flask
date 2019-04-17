from flask import Flask
from celery.task import my_background_task
from celery import Celery
#Importa las librerias

app = Flask(__name__) #nombra flask name a la aplicacion que utilizara
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://'
# configura el broker y el Back end

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# nombra celery a la aplicacion y manda llamar el broker
celery.conf.update(app.config)
# Ni idea, tendra algo que ver con la config. de celery

task = my_background_task.delay(10, 20)
    #Ejecutando la tarea en segundo plano
    #The return value of delay() and apply_async() is an
    # object that represents the task, and this object can be used to obtain STATUS.