from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('proj',
             broker='amqp://',
             backend='amqp://',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()

# A excepcion de  ' add.delay(4, 4) ' todo funciono correctamente, al agregar esta instruccion
# tempo devolvia una larga notacion de numeros y jamas devolvia el la suma que esta dentro de la funcion
# Por lo demas la prueva a sido un exito!