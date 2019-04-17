from flask import Flask, request , render_template

# numero variable global
numero = 0
#necesito otra variable para seguir actualizando las lineas
# nesesito una variable que sera el numero actual y ademas en que sensor va
# la var 'actual' debe mantenerse con cada
# var ronda se mantiene contando hasta llegar el num final de sensores cuando
# Necesito que la maquina haga un loop y mantega el mismo numero de ronda hasta que por fin llegue hasta el final
# mientras que al mismo tiempo puede haber otra ronda a la mitad de la pista
# se puede hacer que cada que sensor 1 se active copie su var a sen2 y asi hasta que cada uno de los sensores terminen de dar la vuelta
# lo malo es que habra que crear una varaible por cada uno de los sensores de esa manera cuando un sensor reciba su senal el pondra ese numero
# en la bd y se lo pasara al siguiente sensor
app = Flask(__name__)

# obteniendo el post resquest
@app.route('/api', methods=['POST'])
def api_response():

    if request.method == 'POST':
        print('Post metodo')

    # aqui obtengo el header que necesito para indentificar dir
    dire = str(request.headers.get('direccion'))
    print('Direccion:', dire )

    # aqui obtengo el header que necesito para indentificar el sensor
    sen_n = str(request.headers.get('sen_n'))
    print('Sensor:', sen_n )

    # aqui obtengo el header que necesito para indentificar el sensor
    num = int(request.headers.get('num'))
    print('Numero:', num )

    global  numero
    numero += 1
    print('Ronda', numero)

    # Esto es lo que se le regresara al sensor
    return "ok"

@app.route("/")
def index():
    return render_template("index.html")