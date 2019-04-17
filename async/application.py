from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
import random
from time import sleep
from threading import Thread, Event

# Configurando flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# Llama a socketIO y lo empareja con con_s
async_mode = None
con_s = SocketIO(app, async_mode=async_mode)

# Contando los usuarios en linea
n_usuarios = 0

# Estos seran los que se encagarar de hacer los 'trabajos' global thread object
hilo = Thread()
# Con stop_hilo se da cuenta si su evento esta activado
stop_hilo = Event()

# crea una clase llamada RandomThread con entrada de variables
class hilo_random(Thread):
    def __init__(self):
        self.delay = 1
        super(hilo_random, self).__init__()

    # Utiliza esta para mandar llamar a self
    def run(self):
        # Con esta comienza la funcion de arriva por defaul
        self.generador_n()

    def generador_n(self):
        print("Making random numbers")

        while not stop_hilo.isSet():
            number = random.randint(0, 50)
            con_s.emit('new', {'el_numero': number}, namespace ='/test')
            print(number)

            # Al ser una tarea infinita por eso esta haciendo stop - No necesitare esto
            sleep(self.delay)


# Index principal
@app.route('/')
def index():
    return render_template('index.html', async_mode=con_s.async_mode)

# Estos son los controles de los sockects para las conexiones
# Este es el socket . on, como vars. de entrada estan 'connect' y namespace =
@con_s.on('connect', namespace='/test')
def test_connect():
    print('Client connected')

    global n_usuarios
    n_usuarios += 1
    print('Numero de usuarios ', n_usuarios)

    # need visibility of the global thread object
    global hilo

    # Con esta funcion revisa que thread este funcionando o no, y lo hecha a andar si no
    if not hilo.isAlive():
        print("Starting Thread")
        # manda llamar a RandomThread
        hilo = hilo_random()
        # Con esto lo hecha a andar
        hilo.start()


#  Funcion socket para desconectar
@con_s.on('disconnect', namespace='/test')
def test_disconnect():
    global n_usuarios
    n_usuarios -= 1
    print('Numero de usuarios', n_usuarios)
    print('Client disconnected')

# configuarando el nombre de las apps y la manera en que correra
if __name__ == '__main__':
    con_s.run(app, debug=True)
