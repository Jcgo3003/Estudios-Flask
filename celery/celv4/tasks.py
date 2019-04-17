import random
import time
from celery import Celery

# Inicia celery y lo configura
app = Celery('tasks', backend='rpc://', broker ='pyamqp://guest@localhost//')

# Este programa ejecutara la tarea en segundo plano
@app.task(bind=True)    # aqui llama a celery y le dice que va haber actualizaciones con bind = True
def long_task(self): # lo actualizara a traves de self
    """Tarea en segundo plano con reporte de esatado"""
    estado = ['bueno', 'mas o menos', 'lento', 'Terrible', 'Colapsado'] # asigna los estados
    mensaje = '' # el mensaje esta vacio pero lo configura como contenedor de letras
    total = 25 # Numero que utilizara para el for y estados importante no modificar esta variable!!!

    for n in range(total):      # esto comenzara a correr la funcion que actualizara resultados
        i = random.randint(0, 4)
        mensaje = '{0}'.format( estado[i] ) # desplegara el mensaje de estado de acuerdo con 'i'

        # actualiza los estados enviando un paquete json a el html
        self.update_state(state='En linea', # state solo sirve para saber cuando termino ni si quiera lo muestra
                          meta={'current': n, 'total': total, # current sera como esta ahora n , total es el final del for, resultado
                                'status': mensaje}) # estatus es el mensaje
        time.sleep(1) # hace que el proceso duerma

    ## esto ocurre cuando terminar el for
    return {'current': 100, 'total': 100, 'status': 'Task completed!', # cuando por fin termina esto es lo que saldra
            'result': 42}




# del original modificare los parametros como
# state que ahora sera state= en linea,
# el meta tendra menos paramentros
# sera uno de los 5 estados que puede bueno mas o menos ..etc.
# No quiero que exista pero es un paramentro esencial

# hasta aqui funciona a la perfeccion
#
# estado = ['bueno', 'mas o menos', 'lento', 'Terrible', 'Colapsado'] # asigna los estados

#     message = '' # el mensaje esta vacio pero lo configura como contenedor de letras
#     total = 6 # total sera un numero al azar entre 10 y 50
#     for i in range(total):      # para i en un rango de total
#         if not message or random.random() < 0.25: # si mensaje negado(si es verdadero ahora es falso) o un # menor que .25
#             message = '{0}'.format(estado[i]),# este sera el mensaje a desplegar

#         self.update_state(state='En linea', # Este self actualizara el state con'progress' y meta sera
#                           meta={'current': i, 'total': total, # current 'i' total = 'total' status 'message'
#                                 'status': message})
#         time.sleep(1) # hace que el proceso duerma por 1 segundo
#     return {'current': 100, 'total': 100, 'status': 'Task completed!', # cuando por fin termina esto es lo que saldra
#             'result': 42}
#
#
# !!!puedo colocar hasta +1 en la lista de estado porque una vez que llega a estado +1 despliega el resultado sin mirar 'estado'


# self.update_state(state='PROGRESS',
#                           meta={'current': i, 'total': total, 'status': message})
#
# si modifico 'state' lo tenfo  que hacer tambien en el html
# state solo lo utliza para controlar cuando recive el resultado y cuando lo despliega



#### DE TODO ESTE CODIGO SOLO ME SIRVE 'message' DESPLIEGA EL RESTULTADO RESULTADO DE 'i'
#### 'i' SERA EL RESULTADO INTERPRETADO POR EL PROGRAMA QUE RECIBE LOS 'POST' RESQUEST


#### Creo que la barra de porcentaje se puede olvidar de momento puesto que solo despliega un porcentage que yo
#### no utilizare para nada por eso
#### LO QUE NO SIRVE ES 'state' PORQUE SOLO MUESTRA EL ESTADO DE LA TAREA !!!!! AUNQUE PODRIA LLEGAR A SER UTIL!!!!!
#### TAMPOCO 'current' PORQUE SOLO MUESTRA EL ESTADO DEL for-loop
#### TAMPOCO 'total' PORQUE SERA UN PROCESO SIN 'FIN' O AL MENOS HASTA QUE TERMINE EL DIA