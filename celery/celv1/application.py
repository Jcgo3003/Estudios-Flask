import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify
from flask_mail import Mail, Message
from tasks import send_async_email, long_task
# !Declara todo lo que necesitara !

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'
# ! Para obtener las variables de entorno !

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.googlemail.com' # servidor de correo
app.config['MAIL_PORT'] = 587   # puerto de correo
app.config['MAIL_USE_TLS'] = True # tls
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') # configurado como variable de entorno
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') # esta tambien
app.config['MAIL_DEFAULT_SENDER'] = 'jbstdump@hotmail.com' # Mail default

# # Celery configuration
# app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
# app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
# # !reconfigurando de redis a mqrabbit

# Initialize extensions
mail = Mail(app)

# # Initialize Celery
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)


# @celery.task # Define la tarea send_async_email y la rellena con 'msg'
# def send_async_email(msg):
#     """Background task to send an email with Flask-Mail."""
#     with app.app_context():  # manda llamar app. app_contexto ()
#         mail.send(msg)       # aqui llama mail.seng y la rellena con 'msg'


# @celery.task(bind=True) #aqui llama a celery y le dice que va haber actualizaciones con bind = True
# def long_task(self): # lo actualizara a traves de self
#     """Background task that runs a long function with progress reports."""
#     verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking'] # asigna a 'verb' bla bla
#     adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast'] # hace lo mismo con abjective
#     noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit'] # y noun
#     message = '' # el mensaje esta vacio pero lo configura como contenedor de letras
#     total = random.randint(10, 50) # total sera un numero al azar entre 10 y 50
#     for i in range(total):      # para i en un rango de total
#         if not message or random.random() < 0.25: # si mensaje negado(si es verdadero ahora es falso) o un # menor que .25
#             message = '{0} {1} {2}...'.format(random.choice(verb),# el mesaje sera un contenedor de 3 espacios cada uno con una seleccion al azar
#                                               random.choice(adjective),
#                                               random.choice(noun))
#         self.update_state(state='PROGRESS', # Este self actualizara el state con'progress' y meta sera
#                           meta={'current': i, 'total': total, # current 'i' total = 'total' status 'message'
#                                 'status': message})
#         time.sleep(1) # hace que el proceso duerma por 1 segundo
#     return {'current': 100, 'total': 100, 'status': 'Task completed!', # cuando por fin termina esto es lo que saldra
#             'result': 42}


@app.route('/', methods=['GET', 'POST']) # para flask para el despliegue de la applicacion principal
def index():
    if request.method == 'GET': # si get regresara el index y de ahi obtendra el correo
        return render_template('index.html', email=session.get('email', ''))
    email = request.form['email'] # email = resquest.form obteniendo el correo del usuario
    session['email'] = email #session guardara el correo electronico directo de email

    # send the email
    msg = Message('Hello from Flask JBST moficated', # agrega el mensaje de flask
                  recipients=[request.form['email']]) # el recipiente sera el correo obtenido por index
    msg.body = 'This is a test email sent from a background Celery task LOVE FROM JBST.' # este sera el cuerpo del mensaje
    if request.form['submit'] == 'Send': # si el botton pinchado es submit
        # send right away
        send_async_email.delay(msg) #enviarlo inmediatamente
        flash('Sending email to {0}'.format(email)) #desplegara enviando correo a ' ' email
    else:
        # send in one minute
        send_async_email.apply_async(args=[msg], countdown=60) # agrando cuenta regresiva al envio
        flash('An email will be sent to {0} in one minute'.format(email))

    return redirect(url_for('index')) # redirige a la pagina principal


@app.route('/longtask', methods=['POST']) # esta es la seccion que hara 'longtask'
def longtask():
    task = long_task.apply_async() #aqui task sera 'long_task'
    return jsonify({}), 202, {'Location': url_for('taskstatus',   # regresara jsonify con 202 para decir que esta trabajando
                                                  task_id=task.id)}


@app.route('/status/<task_id>') # status la parte de flask que se encargara de recibir los estados
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':  # esta es cuando el 'task' no ha comenzado por eso muestra pendiente
        response = {  # respondera con un json que contenga state, current, total y status
            'state': task.state, # state sera llevado por task.state
            'current': 0, # current sera 0
            'total': 1, # total sera 1
            'status': 'Pending...'  # estatus mostrara la palabra pendiente
        }
    elif task.state != 'FAILURE':  # si diferente de failure
        response = { # aqui obtiene los datos utilizando task.info.get para cada uno de las variables
            'state': task.state, # state sera task.state
            'current': task.info.get('current', 0), # current sera task.info.get (current) no se por que el cero
            'total': task.info.get('total', 1), #lo mismo hace para total y status
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result'] # cuando encuentre un resultdo en task.info respodera con la respuesta
    else:
        # something went wrong in the background job
        response = { # esto es si task.state = failure
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised ! aqui dira exatamente que paso al usuario
        }
    return jsonify(response) # despues de esto regresara una respuesta utilizando jsonify


if __name__ == '__main__':
    app.run(debug=True)
#### no tengo idea de que sea esto para parece que es un standar que va al final de cada archivo