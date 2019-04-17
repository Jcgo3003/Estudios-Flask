import random
import time
from celery import Celery

# Inicia celery y lo configura
app = Celery('tasks', backend='rpc://', broker ='pyamqp://guest@localhost//')

# Este programa ejecutara la tarea en segundo plano
@app.task(bind=True)    # va haber actualizaciones con bind = True
def long_task(self):

    """Tarea en segundo plano con reporte de esatado"""

    estado = ['bueno', 'mas o menos', 'lento', 'Terrible', 'Colapsado'] #los estados
    mensaje = ''
    total = 25

    for n in range(total):
        i = random.randint(0, 4)
        mensaje = '{0}'.format( estado[i] ) # mensaje de estado

        # actualiza los estados enviando un paquete json a el html
        self.update_state(state='En linea', meta={'current': n, 'total': total, 'status': mensaje})
        time.sleep(1)

    ## Cuando termina la funcion enviara esto
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42}

