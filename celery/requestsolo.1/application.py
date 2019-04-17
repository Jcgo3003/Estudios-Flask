# Librerias flask
from flask import Flask, request , render_template
# Librerias bd
import sqlite3
import time
import os.path
from datetime import datetime, timedelta

# Nombrando a la aplicacion
app = Flask(__name__)

# Obteniendo el post resquest de los sensores
@app.route('/nes', methods=['POST'])
def api_response():

    if request.method == 'POST':
        ######### Obteniendo datos de los sensores ################
        # Para indentificar dir
        dir = str(request.headers.get('direccion'))
        print('Direccion:', dir )

        # Para indentificar el sensor
        sensor = str(request.headers.get('sen_n'))
        print('Sensor:', sensor )

        # Para indentificar el sensor
        num_sen = int(request.headers.get('num'))
        print('Numero:', num_sen )

        ###################  PORTANDO BDFINAL.py  ##################
        # Creando nombre para la BD apartir de la fecha
        nombrebd = time.strftime('%d%m%y',time.localtime()) + ".db"

        # Lista que se encarga de contar el numero de rondas registradas en la BD
        ron_a = [ 0 , 0 , 0 ]
        ron_b = [ 0 , 0 , 0 ]

        ################ Comienzo - Creando/Leyendo archivo de BD ###############
        # Si ya existe el archivo
        if (os.path.isfile(nombrebd)):
            print("BD existente")

            # Conectando la BD
            conexion = sqlite3.connect(nombrebd)
            print ("Leyendo BD: ", nombrebd)

            # Cursor
            c = conexion.cursor()

            ### Recuperando datos de la DB direccion A #####
            # sen1 - selecciona la columna sen1_a - asigna bd toda esa columna que se guarda como lista - asigna el # de longitud de esa lista
            c.execute("SELECT sen1_a FROM a")
            bd = c.fetchall()
            ron_a[0] = len(bd)

            # sen2 - hace los mismo para la columna de sen2 con algunas diferencias para eliminar las entradas con 'NONE'
            c.execute("SELECT sen2_a FROM a")
            bd = c.fetchall()
            # filtrando las entradas para quitar "NONE" de la lista de entradas
            cuenta = 0
            for i in range (len(bd)):
                if ( str(bd[i][0]) != 'None'):
                    cuenta += 1
            # asigna cuenta a ron_a[1]
            ron_a[1] = cuenta

            # sen3 - Utiliza el mismo metodo para contar en esta columna
            c.execute("SELECT sen3_a FROM a")
            bd = c.fetchall()
            cuenta = 0
            for i in range (len(bd)):
                if ( str(bd[i][0]) != 'None'):
                    cuenta += 1
            ron_a[2] = cuenta

            ### Recuperando datos de la DB  para la vuelta  direccion B ##### Hace exactamente lo mismo pero para las columnas en B
            # sen3
            c.execute("SELECT sen3_b FROM b")
            bd = c.fetchall()
            ron_b[2] = len(bd)

            # sen2
            c.execute("SELECT sen2_b FROM b")
            bd = c.fetchall()
            cuenta = 0
            for i in range (len(bd)):
                if ( str(bd[i][0]) != 'None'):
                    cuenta += 1
            ron_b[1] = cuenta

            # sen1
            c.execute("SELECT sen1_b FROM b")
            bd = c.fetchall()
            cuenta = 0
            for i in range (len(bd)):
                if ( str(bd[i][0]) != 'None'):
                    cuenta += 1
            ron_b[0] = cuenta
            # En este punto ya tenemos las listas de rondas con la cuenta exacta de la ultima entrada
            # De esta manera se reanundan los registros en donde se quedaron

        # Creando la BD nueva
        else:
            # En caso de que no exista la base de datos crea una completamente vacia
            print("Creando BD ...")
            # Creando BD
            conexion = sqlite3.connect(nombrebd)
            print ("Base de datos creada: ", nombrebd)

            # Cursor para la bd
            c = conexion.cursor()

            # creando tablas
            # Crea tabla 'a' con 'num_a' - registro de rondas, Sen1_a - hora de registro, Sen2_a - hora de registro, Sen3_a - hora de registro.
            c.execute(''' CREATE TABLE "a" ('num_a' INTEGER PRIMARY KEY , 'sen1_a' TIME, 'sen2_a' TIME, 'sen3_a' TIME )''')
            # Crea tabla 'b' con 'num_b' - registro de rondas, Sen1_b - hora de registro, Sen2_b - hora de registro, Sen3_b - hora de registro.
            c.execute(''' CREATE TABLE "b" ('num_b' INTEGER PRIMARY KEY , 'sen3_b' TIME, 'sen2_b' TIME, 'sen1_b' TIME )''')

        # Imprimiendo estado de la bd
        print('Las rondas comienzan asi A', ron_a)
        print('Las rondas comienzan asi B', ron_b)
        print()

        ################ Introduccion de datos a la DB# #########################
        # Seccion para insertar los datos en la bd 'a' ...
        if ( dir == 'a'):
            # Crendo un nueva linea en la BD, por ser el sensor 1 se crea una nueva linea en la bd
            if (num_sen == 1 ):
                # sumando +1 al contador de rondas
                ron_a[0] += 1

                # Asegurando que el registro sea un registro 'esperado' y no un error de lectura
                # igual le pondre un limite de maximo 5 entradas arriva que el resto solo por precaucion
                if (ron_a[0] >= (ron_a[1] + 6)):
                    print('Error, no se puede guardar el registro Sen1_a  ya tiene demasiados registros')
                    # Quitando el +1 que se agrego arriva y salir sin guardar nada
                    ron_a[0] -= 1
                else:
                    print("Guardando registro a Dir a, sen%s_a" % (num_sen))

                    # obteniendo la hora exacta de ese momento para guardarla en hora_now
                    hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                    # introduciendo el # de ronda en 'num_a', en la en columna sen1_a, en las demas 'NONE'
                    c.execute('''INSERT INTO a ("num_a","sen1_a","sen2_a","sen3_a") VALUES ( ? , ? ,NULL,NULL)''', (ron_a[0], hora_now) )

            # Otros sensores
            else:
                # se resta 1 la numero del sensor para hace que corresponda con numero de sitio de la lista de rondas
                num_sen -= 1
                ron_a[num_sen] += 1

                # protegiendo la lista
                if ((ron_a[num_sen] > ron_a[num_sen-1])):
                    print("Error no se puede agregar registro a Dir a, sen%s_a no se espera a registrar en este momento" % (num_sen+1))
                    # Se le quita un numero a la ronda que ya habia guardado y no se guarda nada
                    ron_a[num_sen] -= 1

                else:
                    # Si pasa el filtro se guarda el registro
                    print("Guardando registro a Dir a, sen%s_a" % (num_sen+1))

                    # Se obtiene la hora actual y se guarda en hora_now
                    hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                    # Actualiza los datos, donde estaba 'NONE' ahora estara el valor de hora_now
                    # Utiliza sensor - columna, hora_now para el registro, ron_a[num_sen] para colocarlo en la linea correcta
                    c.execute('''UPDATE a SET {} = ? where num_a = ? '''.format( sensor), (hora_now, ron_a[num_sen] ) )

        # Seccion para insertar los datos en la bd 'b' ...
        else:
            # Se utiliza el mismo metodo diferente orden al ser el sensor 3 el que empieza, porque el sensor estara
            # Colocado en la ultima estacion de dir. 'a', haciendo que sensor 3 sea la primera en activarse y crea la linea
            if (num_sen == 3 ):

                # Agrega +1 a su cuenta de rondas de nuevo al ser sen3 el primero de dir. 'b' la lista se actulizara de derecha a izquierda
                ron_b[2] += 1

                # Asegurando que el registro sea un registro 'esperado' y no un error de lectura
                # tiene un limite de maximo 5 entradas arriva que el resto solo por precaucion
                if ( ron_b[2] >= ( ron_a[1] + 6) ):
                    print('Error, no se puede guardar el registro sen2_b  ya tiene demasiados registros')
                    # Quitando el +1 que se agrego arriva y salir sin guardar nada
                    ron_b[2] -= 1
                else:
                    print("Guardando registro a Dir b, sen%s_b" % (num_sen))

                    # obteniendo la hora actual y guardandola en hora_now
                    hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                    # Creando la nueva linea
                    c.execute('''INSERT INTO b ("num_b","sen3_b","sen2_b","sen1_b") VALUES ( ? , ? ,NULL,NULL)''', (ron_b[2], hora_now) )

            # Otros sensores en 'b'
            else:
                # Al igual que en 'a' aqui actualizara los datos de esas columnas pasando los 'NONE's a registros de tiempo

                # para que las rondas se guarden correctamente
                num_sen -= 1

                # Sumando +1 a la lista de rondas 'b'
                ron_b[num_sen] += 1

                # protegiendo la lista
                if ((ron_b[num_sen] > ron_b[num_sen+1])):
                    print("Error no se puede agregar registro a Dir b, sen%s_b no se espera a registrar en este momento" % (num_sen+1))
                    # Se le quita un numero a la ronda que ya habia guardado y no se guarda nada
                    ron_b[num_sen] -= 1

                else:
                    # Si pasa el filtro se guarda el registro
                    print("Guardando registro a Dir b, sen%s_b" % (num_sen+1))

                    # obteniendo la hora acutal
                    hora_now = (time.strftime('%H:%M:%S',time.localtime()))
                    # Actulizando los datos utilizando el num. de rondas para colocarlo en su sitio correctamente, hora_now para hacer el registro y num_sen para su columna
                    c.execute('''UPDATE b SET {} = ? where num_b = ? '''.format(sensor), (hora_now, ron_b[num_sen] ) )

        # Con esta linea se guardan los registros definitivamente el la bd
        conexion.commit()
        # cerrando conexiones con la bd
        conexion.close()

        # Imprime el estado de la rondas
        print('Las rondas terminan asi A', ron_a)
        print('Las rondas terminan asi B', ron_b)
        print()

        # Esto es lo que se le regresara al sensor
        return "ok"

    # Evitando errores al hora de recibir otro tipo de request no deseados
    else:
        return 'Error de submicion de datos'


@app.route("/admin")
def index():
    return render_template("index.html")