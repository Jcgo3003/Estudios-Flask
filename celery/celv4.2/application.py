# Esta version eliminara toda la seccion de correo, intentara crear un proceso ficticio
# E intentara monitorearlo

import os
from flask import Flask, request, render_template, session, flash, redirect, url_for, jsonify
# Esta es la funcion que esta en task.py
from tasks import long_task


# Por alguna razon no puedo borrar esto, tiene que ver con 'session'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nadiesabe'


# despliegue de la pagina principal
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET': # si get regresara el index y de ahi obtendra el correo
        return render_template('index.html')# return redirect(url_for('index')) # redirige a la pagina principal
# Pagina para arrancar aplicacion en segundos
@app.route('/ini', methods=['GET'])
def ini():
    if request.method == 'GET':
        return render_template('ini.html')


# esta es la seccion que hara 'longtask'
@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async(task_id = '182') #aqui task sera 'long_task'
    return jsonify({}), 202, {'respuesta': url_for('taskstatus',   # regresara jsonify con 202 para decir que esta trabajando
                                                  task_id=task.id)}


# status la parte de flask que se encargara de recibir los estados
@app.route('/status/<task_id>')
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