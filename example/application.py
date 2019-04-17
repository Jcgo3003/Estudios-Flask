#!/usr/bin/env python
from threading import Lock
# Importa los clasicos de siempre
from flask import Flask, render_template, session, request
# Pero aqui ya importa todo lo que nos sera util a la hora de actualizar
# muchas funciones no me seran utiles como la de join_room, leave_room y close room.
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

# Ajusta flask
app = Flask(__name__)
# Clave secreta de session - secret
app.config['SECRET_KEY'] = 'secret!'
# crea socketio y le asigna la funcion SocketIO  con dos variables
socketio = SocketIO(app, async_mode=async_mode)
# Esto tiene que ver con las aplicacones thread
thread = None
thread_lock = Lock()

# Crea la aplicacion background_thread
def background_thread():
    """Example of how to send server generated events to clients."""
    # count = 0
    count = 0
    # Comienza un while loop de para siempre
    while True:
        # socketio.sleep 10, activa socketio, cada 10 segundos o algo asi
        socketio.sleep(10)
        # Agrega a cuenta 1
        count += 1
        # Y depues manda llamar esa misma funcion para emitir en los holders
        # my_response,                  empaquetado entre corcheas
        # {data : 'El evento generado por el servidor', cuenta: count, } ,
        # namespace = /test ------- Unico que llama al final a /test
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

# La app principal para hacer render del Index
@app.route('/')
def index():
    # manda render el index, y asigna el modo de sinconizacion a asincrono
    return render_template('index.html', async_mode=socketio.async_mode)

#Enciende a socketio con las variables my_evento y llama a /test
# socketio.on con variables 'my_event', y namespace= /test
@socketio.on('my_event', namespace='/test')
def test_message(message):
    # Llama a session y la ajusta para obtener la cuenta de count de background
    # session 'recibe_cuenta' = session.obtener 'obtener cuenta', 0 y a eso le suma 1
    session['receive_count'] = session.get('receive_count', 0) + 1
    # Emite, my_response, { datos: mensaje[dato], cuenta: session [recibe cuenta]
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


# Enciende otro socket y lo llena con las variables de abajo, siempre llama a /test
# 'my_broadcast_event'
@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    # Session [recive_cuenta] y hace exactamente lo mismo que arriva
    session['receive_count'] = session.get('receive_count', 0) + 1
    # emite my_response, datos: mensaje[dato], cuenta[ session recive cuenta]
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)



# otra vez hace lo mismo de encender el socketio, rellenando con join y llamando a /test
@socketio.on('join', namespace='/test')
def join(message):
    # Aqui hay un cambio, join_room(message['room'))
    # me parece que las variables las recibe del INDEX
    join_room(message['room'])
    # Session recibe cuenta = session obtener cuenta + 1
    session['receive_count'] = session.get('receive_count', 0) + 1
    # emit my_response, dato: 'In rooms:'  + agregando ',' join(rooms()), cuenta [session]
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

# llena con leave, llama de nuevo a /test
@socketio.on('leave', namespace='/test')
def leave(message):
    # rellena leave_room(mensaje[room])
    leave_room(message['room'])
    # Session recibe el numero = session obtener recibe cuenta, 0 + 1
    session['receive_count'] = session.get('receive_count', 0) + 1
    # my_response, data: 'In room:' + agrega ', ' .join(room), cuenta [session]
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})

# cierra cuarto
@socketio.on('close_room', namespace='/test')
# en todas las funciones esta recibieno info de message
def close(message):
    # Recibe cuenta de session = session.obtener('recibe_cuenta', 0) + 1
    session['receive_count'] = session.get('receive_count', 0) + 1
    # my_response, { data: 'room' + message[cuarto] + 'esta cerrando', cuenta = session
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
        # cuarto = mensaje [cuarto], cierra_cuarto[cuarto]
         room=message['room'])
    close_room(message['room'])

# Evento de cuarto, de nuevo llama a /test
@socketio.on('my_room_event', namespace='/test')
# En todas y cada una de las funciones entra (messajes)
def send_room_message(message):
    # de nuevo esta funcion para agregar + 1 a session count
    session['receive_count'] = session.get('receive_count', 0) + 1
    # Aqui emite todo igual excepto porque al final emite room_mesasge = room
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])

# A socketio.on le llama disconnet_request , y llama de nuevo a /test
@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    # + 1 a count
    session['receive_count'] = session.get('receive_count', 0) + 1
    # en emit envia como datos str y datos de otras funciones
    # siempre hace que session cuente
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    # aqui simplemente desconecta
    disconnect()

# my_ping, /test
@socketio.on('my_ping', namespace='/test')
# Este no acepta ninguna variable
def ping_pong():
    #emite 'my_pong'
    emit('my_pong')

# para conectar, de nuevo /test
@socketio.on('connect', namespace='/test')
# Tampoco acepta ninguna variable
def test_connect():
    # utiliza de global a thread
    global thread
    # le agrega thread_lock
    with thread_lock:
        # si thread es nulo
        if thread is None:
            # Lo configura como el cree que es que mejor
            # thread = socketio.comienza a 'tare en segundo plano'
            #           Lo comienza con las variables target = hilo secundario
            thread = socketio.start_background_task(target=background_thread)
    # esta vez emite muy poca informacion
    # simpre emite my_reponse como str, y empaqueta estos datos
    emit('my_response', {'data': 'Connected', 'count': 0})

# otro disconnect???
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    # imprime en pantalla 'client disconnected' con el request.sid
    print('Client disconnected', request.sid)

# configura a flaks
if __name__ == '__main__':
    socketio.run(app, debug=True)


#   Utiliza a session como para mantener algunos numeros como variable global
#   'emit' envia datos empaquetados al index pero apenas cambia los datos de cada paquete
# Casi en cada funcion agrega session para agregarle + 1 a session count
