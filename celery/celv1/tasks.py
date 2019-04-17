import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from flask_mail import Mail, Message
from celery import Celery
import random
# from flask import Flask, request, render_template, session, flash, redirect, \
#     url_for, jsonify
# app = Flask(__name__)

# Celery configuration !reconfigurando de redis a mqrabbit
# app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
# app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

#app = Celery('tasks', backend='rpc://', broker ='pyamqp://guest@localhost//')

# @app.task
# def add(x, y):
#     z = x + y
#     return (z)


# Initialize Celery
app = Celery('tasks', backend='rpc://', broker ='pyamqp://guest@localhost//')
# celery.conf.update(app.config)


@app.task # Define la tarea send_async_email y la rellena con 'msg'
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    with app_context():  # manda llamar app. app_contexto ()
        mail.send(msg)       # aqui llama mail.seng y la rellena con 'msg'


@app.task(bind=True) #aqui llama a celery y le dice que va haber actualizaciones con bind = True
def long_task(self): # lo actualizara a traves de self
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking'] # asigna a 'verb' bla bla
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast'] # hace lo mismo con abjective
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit'] # y noun
    message = '' # el mensaje esta vacio pero lo configura como contenedor de letras
    total = random.randint(10, 50) # total sera un numero al azar entre 10 y 50
    for i in range(total):      # para i en un rango de total
        if not message or random.random() < 0.25: # si mensaje negado(si es verdadero ahora es falso) o un # menor que .25
            message = '{0} {1} {2}...'.format(random.choice(verb),# el mesaje sera un contenedor de 3 espacios cada uno con una seleccion al azar
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS', # Este self actualizara el state con'progress' y meta sera
                          meta={'current': i, 'total': total, # current 'i' total = 'total' status 'message'
                                'status': message})
        time.sleep(1) # hace que el proceso duerma por 1 segundo
    return {'current': 100, 'total': 100, 'status': 'Task completed!', # cuando por fin termina esto es lo que saldra
            'result': 42}