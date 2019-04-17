from tasks import add
from flask import Flask, redirect, render_template, session, url_for

app = Flask(__name__)

@app.route("/")
def index():
    tempo = add(4, 2)
    print(tempo)
    return render_template("index.html", tempo=tempo)

# A excepcion de  ' add.delay(4, 4) ' todo funciono correctamente, al agregar esta instruccion
# tempo devolvia una larga notacion de numeros y jamas devolvia el la suma que esta dentro de la funcion
# Por lo demas la prueva a sido un exito!