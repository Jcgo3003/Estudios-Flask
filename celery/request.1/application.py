from flask import Flask, request , render_template
import sqlite3
import time
import os.path

app = Flask(__name__)

# obteniendo el post resquest
@app.route('/api', methods=['GET','POST'])
def api_response():

    # Identificando el sensor y obteniendo su tiempo
    if request.method == 'POST':
        # Datos sensor
        sen_dir = (request.headers.get('dir'), )
        num_sen = (request.headers.get('sensor'), )
        tiempo_sen = (time.strftime('%H:%M:%S',time.localtime()),  )

        # Nombrando la bd # IMPORTANTE revisar el nombre con respecto el dia
        nombrebd = time.strftime('%d%m%ys',time.localtime()) + ".db"

        # Comprobando si ya existe la bd
        if (os.path.isfile(nombrebd) ):
            print("base existe")
        else:
            print("base no existe")
            # Creando BD
            conexion = sqlite3.connect(nombrebd)
            print ("Base de datos creada con el nombre", nombrebd)

            # Cursor
            c = conexion.cursor()

            # creando tablas
            #crear tabla con direciona a   ###################
            c.execute(''' CREATE TABLE "sens_dir_a" ('num' INTEGER PRIMARY KEY AUTOINCREMENT, 'sen1_a' TIME, 'sen2_a' TIME, 'sen3_a' TIME )''')
            #crear tabla con direcion b
            c.execute(''' CREATE TABLE "sens_dir_b" ('num' INTEGER PRIMARY KEY AUTOINCREMENT, 'sen1_b' TIME, 'sen2_b' TIME, 'sen3_b' TIME )''')


        # Conectando la bd - Misma funcion que para crear BD
        conexion = sqlite3.connect(nombrebd)
        print ("Base de datos creada con el nombre", nombrebd)

        # Cursor
        c = conexion.cursor()

        # agregando datos
        if (num_sen == 1 or num_sen == 3):
            #insertando primer tiempo sensor1 a ################################
            c.execute('''INSERT INTO "sens_dir_a" ("num","sen1_a","sen2_a","sen3_a") VALUES ( ' ' , tiempo_sen ,NULL,NULL)''')
        else:
            #leer el numero actual de la base de datos ??
            c.execute('''UPDATE "sens_dir_a" SET "sen2_a" = '12:05:06' where num = 1''')



    # Respuesta al sensor
    return "ok"




@app.route("/")
def index():
    return render_template("index.html")


# Dependiendo del numero del sensor variaran sus reglas
# sensor1_a o el sensor ultimo_b  agregaran numero y su tiempo pero solamente ellos, ellos siempre abren jamas actulizan
# los demas sensores solo pueden actulizar datos