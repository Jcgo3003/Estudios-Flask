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
    # aqui obtengo el header que necesito para indentificar el sensor
    n = 0
    n = int(request.headers.get('sensor'))
    if  (n == 1):
        global  numero
        numero += 1
        print('numero', numero)
    if request.method == 'POST':
       print('post metodo')
       print(n)
    # Esto es lo que se le regresara al sensor
    return "ok"

@app.route("/")
def index():
    return render_template("index.html")