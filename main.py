import Individuo
import Poblacion
from Individuo import Individuo
from Poblacion import Poblacion
from GB import genetico_basico

import time







def genetico(numero_poblacion=30,segundos_ejecucion=100,alpha=4):
    start_time = time.time()
    diff_time = 0

    poblacion = Poblacion(numero_poblacion,alpha=alpha)


    while(diff_time < segundos_ejecucion):
        print(diff_time)
        poblacion.actualizar_poblacion()
        poblacion.calcular_elite()
        poblacion.cruze_2_puntos_con_mutacion()
        
        # poblacion.mutar_poblacion()
        # poblacion.actualizar_poblacion()
        diff_time = (time.time() - start_time)
        
    print(poblacion.individuos)



genetico(segundos_ejecucion=4000,alpha=2)


    



# genetico_basico(numero_individuos=10)