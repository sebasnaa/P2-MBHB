# from random import random
import copy
import random
import numpy as np
import Individuo
import Poblacion
from Individuo import Individuo
from Poblacion import Poblacion

import time


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import algoritmosV2



def genetico(numero_poblacion=30,generaciones_limite = 5000,segundos_ejecucion=100,alpha=4,verbose=False):
    
    historico_km = []
    historico_slots = []
    segundos = []
    start_time = time.time()
    diff_time = 0
    poblacion = Poblacion(numero_poblacion,alpha=alpha,numero_elites=5)

    historico_km.append(poblacion.individuos[0].km)
    historico_slots.append(poblacion.individuos[0].contenido.sum())
    segundos.append(0)
    generacion = 0
    
    # plt.ion()
    # fig = plt.figure()
    # x = []
    # x.append(diff_time)
    # y = []
    # y2 = []
    # y.append(poblacion.individuos[0].km)
    # y2.append(poblacion.individuos[0].contenido.sum())
    
    while(generacion < generaciones_limite):
        
        # new_y=poblacion.individuos[0].km
        # new_y2 = poblacion.individuos[0].contenido.sum()
        # x.append(diff_time)
        # y.append(new_y)
        # y2.append(new_y2)
        # # plt.scatter(diff_time,new_y,marker='*')
        # plt.plot(diff_time,new_y, ls='solid',marker=0, color='b', label='line with marker')
        # plt.plot(diff_time,new_y2, ls='solid',marker='*', color='r', label='line with marker')
        # plt.show()
        # plt.pause(0.1) 
        
        
        print(diff_time , " ", generacion)
        poblacion.actualizar_poblacion()
        poblacion.calcular_elite()
        poblacion.cruze_2_puntos_con_mutacion()
        segundos.append(diff_time)
        historico_km.append(poblacion.individuos[0].km)
        historico_slots.append(poblacion.individuos[0].contenido.sum())
        diff_time = (time.time() - start_time)
        generacion+= 1

    if(verbose):
        print(poblacion.individuos)
        # plt.plot(segundos, historico_km)
        # plt.plot(segundos, historico_slots)
        # plt.legend(["KM", "Slots"])
        # plt.show()
        
    return poblacion.individuos

  

def chc(numero_poblacion=30,alpha=6,reinicios_salida = 1,numero_elite = 5):
    poblacion = Poblacion(numero_poblacion,alpha=alpha)
    print("poblacion Inicial")
    print(poblacion.individuos)
    reinicios = 0
    distancia_umbral = 4
    poblacion_tmp = []
    start_time = time.time()
    diff_time = 0
    
    sol_ini = copy.deepcopy(poblacion.individuos[0])
    
    # diff_time = (time.time() - start_time)
    # reinicios < reinicios_salida
    while(diff_time < 100):
        print(diff_time)
        # print(poblacion.individuos[0])
        
        poblacion_tmp = copy.deepcopy(poblacion.individuos)
        
        # poblacion_tmp = poblacion.individuos.copy()
        
        indices_padres_desordenados = algoritmosV2.calcular_indices_padres_desordenados(poblacion.numero_individuos)
        
        for k in range(0,poblacion.numero_individuos-1,2):
            padre =  copy.deepcopy(poblacion.individuos[indices_padres_desordenados[k]])
            madre =  copy.deepcopy(poblacion.individuos[indices_padres_desordenados[k+1]])
            dis_padres,posiciones_diferentes = algoritmosV2.distancia_hamming(padre,madre,diferencia_permitida = 0)
            if(dis_padres > distancia_umbral):
                
                hijo_1,hijo_2 = algoritmosV2.blx_alpha_pc(padre,madre,posiciones_diferentes)
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
    
    print("poblacion final con nº reeiniciaio ", reinicios)
    print(poblacion.individuos)
    print("inicio ")
    print(sol_ini)
    # print(poblacion.individuos)
    # print("ant")
    # print(poblacion_tmp)        
    
  
    
    
def multi_modal(numero_poblacion=30,segundos_ejecucion=20,alpha=5,radio = 4):
 
    start_time = time.time()
    diff_time = 0
    poblacion = Poblacion(numero_individuos=numero_poblacion,alpha=alpha,numero_elites=5)
    
    
    generacion = 0
    # cada generacion necesita +- 0.0200000000000000 s
    while(generacion < 100):       
        
        print(diff_time)
        poblacion.actualizar_poblacion()
        poblacion.calcular_elite()
        poblacion.cruze_2_puntos_con_mutacion()
        diff_time = (time.time() - start_time)
        if(generacion % 5 == 0):
            nichos = poblacion.clearing(radio=radio)
            poblacion.cruze_2_puntos_con_mutacion(clearing=True)
        generacion += 1
        
    print(poblacion.individuos)    
    print("nichos")
    # print(nichos)
    
    
    
random.seed(132456987)
np.random.seed(132456987)
genetico(generaciones_limite = 6000,alpha=5,verbose=True)

# chc(numero_poblacion=30,alpha=5,reinicios_salida = 1)

# multi_modal(numero_poblacion=10,alpha=5,radio=4,segundos_ejecucion=10)



