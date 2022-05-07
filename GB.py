import copy
import Individuo
import Poblacion
from ind_aux import ind_aux
from Poblacion import Poblacion


import time


import algoritmos
import random
import numpy as np


def actualizar_individuo(individuo):
    aux = copy.deepcopy(individuo)
    slots_diff = aux.contenido.sum()-205
    if slots_diff > 0 :
        aux.fitness = algoritmos.coste_slot(aux.contenido) + aux.alpha*slots_diff
    else:
        aux.fitness = algoritmos.coste_slot(aux.contenido)
    return aux

def calcular_elite(poblacion):
    sortedByFitness = sorted(poblacion,key=lambda k: k.fitness)
    elite = sortedByFitness[0:5]
    return elite

def cruze_dos_puntos(poblacion,elite):
    hijos = copy.deepcopy(elite)
    # hijos = []
    numero_hijos_creados = 0
    
    while(len(hijos) < len(poblacion)):
        padre =    copy.deepcopy(poblacion[random.choice(np.arange(0,len(poblacion)))]) 
        
        madre = copy.deepcopy(poblacion[random.choice(np.arange(0,len(poblacion)))])

        punto_corte_a = 0
        punto_corte_b = 0
        distanciamiento = abs(punto_corte_b - punto_corte_a)
    
        while distanciamiento > 5 or punto_corte_a == punto_corte_b:
            punto_corte_a = random.choice(np.arange(0,15))
            punto_corte_b = random.choice(np.arange(0,15))
            distanciamiento = abs(punto_corte_b - punto_corte_a)
        
        if punto_corte_b < punto_corte_a:
                punto_corte_a, punto_corte_b = punto_corte_b,punto_corte_a
                
         # hijo formado por padre y segmento de madre    
        hijo_1 = copy.deepcopy(padre)
        hijo_1.contenido[punto_corte_a:punto_corte_b] = madre.contenido[punto_corte_a:punto_corte_b].copy()
        
        # # hijo formado por madre y segmento de padre  
        hijo_2 = copy.deepcopy(madre)
        hijo_2.contenido[punto_corte_a:punto_corte_b] = padre.contenido[punto_corte_a:punto_corte_b].copy()

        if(hijo_1.contenido.sum() > 205):
            tmp = actualizar_individuo(hijo_1)
            hijos.append(tmp)

        if(hijo_2.contenido.sum() > 205):
            tmp = actualizar_individuo(hijo_2)
            hijos.append(tmp)

    return hijos[0: len(poblacion)]


def mutar_poblacion(poblacion,elite):
    nueva_poblacion_mutada = copy.deepcopy(poblacion)
    
    for i in range(len(nueva_poblacion_mutada)):
        nueva_poblacion_mutada[i].mutar()
        # nueva_poblacion_mutada[i] = copy.deepcopy(actualizar_individuo(nueva_poblacion_mutada[i]))
            
    return nueva_poblacion_mutada
    
    

def genetico_basico(numero_individuos = 10,alpha = 1.5):
    
    poblacion = []
    for i in range(numero_individuos):
        ind =  ind_aux()
        poblacion.insert(i,ind)

    # print(poblacion)
    # repetir 
    start_time = time.time()
    diff_time = 0
    
    ite = 0
    while(diff_time < 20):
    
        # calculo de la elite que se conserva en la siguiente generacion
        elite = calcular_elite(poblacion)
        # print("elite")
        # print(elite)
        
        poblacion = cruze_dos_puntos(poblacion=poblacion,elite=elite)
        # print(len(poblacion))
        # print("antes de mutacion")
        # print(poblacion)
        
        # mutamos la poblacion
        print("tras mutacion")
        poblacion = mutar_poblacion(poblacion=poblacion,elite=elite)
        print(poblacion)
        
        diff_time = (time.time() - start_time)
    
    print(poblacion)