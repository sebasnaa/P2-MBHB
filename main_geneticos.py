import copy
import random
import numpy as np
import pandas as pd
import Individuo
import Poblacion
from Individuo import Individuo
from Poblacion import Poblacion

import time


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import algoritmosV2



def genetico(numero_poblacion=30,generaciones_limite = 5000,segundos_ejecucion=100,alpha=5,verbose=False):
    
    start_time = time.time()
    diff_time = 0
    poblacion = Poblacion(numero_poblacion,alpha=alpha,numero_elites=5)
    generacion = 0
    
    contador = 30
    
    while(generacion < generaciones_limite):

        # print(diff_time , " ", generacion)
        
        
        poblacion.actualizar_poblacion()
        contador += 30
        poblacion.calcular_elite()
        poblacion.cruce_2_puntos_con_mutacion()
        
   
        diff_time = (time.time() - start_time)
        generacion+= 1
        
        # if(generacion == generaciones_limite/2):
        #     print("mitad")
        #     print(poblacion.individuos)

    if(verbose):
        print("numero llamadas  " , contador)
        print(poblacion.individuos)
        
    

  

def chc(numero_poblacion=30,alpha=6,generaciones_limite=500,distancia_umbral = 6,numero_elite = 5):
    poblacion = Poblacion(numero_poblacion,alpha=alpha)
    reinicios = 0
    poblacion_tmp = []
    start_time = time.time()
    diff_time = 0
    
    sol_ini = copy.deepcopy(poblacion.individuos[0])
    generacion = 0
    historico = []
    historico.append(poblacion.individuos[0])
    
    contador = 30
    
    while(generacion < generaciones_limite):
        print(diff_time, "  ", generacion)
        
        
        # if(generacion == generaciones_limite/2):
        #     print("mitad")
        #     print(poblacion.individuos)
        
        poblacion_tmp = copy.deepcopy(poblacion.individuos)
        historico.append(poblacion.individuos[0])
        # poblacion_tmp = poblacion.individuos.copy()
        
        indices_padres_desordenados = algoritmosV2.calcular_indices_padres_desordenados(poblacion.numero_individuos)
        
        for k in range(0,poblacion.numero_individuos-1,2):
            padre =  copy.deepcopy(poblacion.individuos[indices_padres_desordenados[k]])
            madre =  copy.deepcopy(poblacion.individuos[indices_padres_desordenados[k+1]])
            dis_padres,posiciones_diferentes = algoritmosV2.distancia_hamming(padre,madre,diferencia_permitida = 0)
            if(dis_padres > distancia_umbral):
                
                hijo_1,hijo_2 = algoritmosV2.blx_alpha_pc(padre,madre,posiciones_diferentes)
                contador += 2
               
                poblacion.individuos.append(hijo_1)
                poblacion.individuos.append(hijo_2)
                
        
        poblacion.individuos = sorted(poblacion.individuos,key=lambda k: k.fitness)
        poblacion.individuos = poblacion.individuos[0:poblacion.numero_individuos]

        
        iguales = algoritmosV2.comparar_poblaciones(poblacion_anterior=poblacion_tmp,poblacion=poblacion)
        
        
        if(iguales):
            distancia_umbral -= 1
        
        if(distancia_umbral == 0):
            # modificamos la poblacion cogemos el 10% de los mejores individuos 
            # y el resto se crean de forma aleatoria
            for i in range(numero_elite,poblacion.numero_individuos):
                ind = Individuo(alpha=alpha)
                poblacion.individuos[i] = copy.deepcopy(ind)
            distancia_umbral = 4
            reinicios += 1
        diff_time = (time.time() - start_time)
        generacion += 1
        
        
    
    print("poblacion final con nº reeiniciaio ", reinicios , " costes ", contador)
    print(poblacion.individuos)
    
    return historico
    
  
    
    
def multi_modal(numero_poblacion=30,generaciones_limite=100,alpha=5,radio = 4):
 
    start_time = time.time()
    diff_time = 0
    poblacion = Poblacion(numero_individuos=numero_poblacion,alpha=alpha,numero_elites=5)
    
    
    generacion = 0
    contador = 30
    while(generacion < generaciones_limite): 
        
        if(generacion == generaciones_limite/2):
            print("mitad")
            print(poblacion.individuos)      
        
        # print(diff_time, " ", generacion)
        poblacion.actualizar_poblacion()
        contador += 30
        poblacion.calcular_elite()
        poblacion.cruce_2_puntos_con_mutacion()
        diff_time = (time.time() - start_time)
        
        if(generacion % 5 == 0):
            nichos = poblacion.clearing(radio=radio)
            poblacion.cruce_2_puntos_con_mutacion(clearing=True)
        generacion += 1
        
    print("numero costes ", contador)
    print(poblacion.individuos)    
    print("nichos")
    



#####################################
#-----------------------------------#
#####################################


# random.seed(258741369)
# np.random.seed(258741369)

random.seed(132456987)
np.random.seed(132456987)


# historico = genetico(generaciones_limite = 10_000,alpha=5,verbose=True)

# chc(numero_poblacion=30,alpha=5,generaciones_limite=10_000,distancia_umbral = 4)

multi_modal(numero_poblacion=30,generaciones_limite=10_000,alpha=5,radio=4)



