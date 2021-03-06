import copy
import itertools
import math
import numbers
from re import L

import matplotlib.axis
import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np
import random
import time
from numpy import genfromtxt
from sympy import true


 


def modificar_datos_acciones(fichero_acciones):

    filas = fichero_acciones.shape[0]
    columnas = fichero_acciones.shape[1]
    salida = []
    for f in range(filas):
        for c in range(columnas):
            if not fichero_acciones[f][c] == 0:
                salida.append((c, fichero_acciones[f][c]))

    return salida


################## Inicializar variables ficheros



indices = genfromtxt('datos/cercanas_indices.csv', delimiter=',')
indicesMod = np.delete(indices, 0, 0)

kmRelativos = genfromtxt('datos/cercanas_kms.csv', delimiter=',')
kmRelativosMod = np.delete(kmRelativos, 0, 0)

acciones = genfromtxt('datos/deltas_5m.csv', delimiter=',')
bicicletas_objetivo_iniciales = acciones[1]
accionesMod = np.delete(acciones, 0, 0)
accionesMod = np.delete(accionesMod, 0, 0)

lista_acciones = modificar_datos_acciones(accionesMod*2)









def accion_posible(bicicletas_input,estacion,bicicletas_en_slots,huecos_disponibles_en_slots):
    # queremos guardar bicis
    # estacion =  estacion -1
    if(bicicletas_input>0):
        if huecos_disponibles_en_slots[estacion] >= bicicletas_input:
            bicicletas_en_slots[estacion] = bicicletas_en_slots[estacion]+bicicletas_input
            huecos_disponibles_en_slots[estacion] = huecos_disponibles_en_slots[estacion]-bicicletas_input
            return 0,bicicletas_en_slots,huecos_disponibles_en_slots
        elif huecos_disponibles_en_slots[estacion] >0:
            while huecos_disponibles_en_slots[estacion] > 0:
                bicicletas_input = bicicletas_input-1
                bicicletas_en_slots[estacion] = bicicletas_en_slots[estacion] + 1
                huecos_disponibles_en_slots[estacion] = huecos_disponibles_en_slots[estacion] - 1
            return bicicletas_input,bicicletas_en_slots,huecos_disponibles_en_slots
        else:
            return bicicletas_input,bicicletas_en_slots,huecos_disponibles_en_slots
    else:
        #queremos sacar bicis
        #se utiliza un valor negativo en bicicletas_input por tanto *-1
        aux = (bicicletas_input *(-1))
        if bicicletas_en_slots[estacion] >= aux:
            #se suma un valor neg por tanto se resta
            bicicletas_en_slots[estacion] = bicicletas_en_slots[estacion]-aux
            #se resta un valor neg por tanto se suma
            huecos_disponibles_en_slots[estacion] = huecos_disponibles_en_slots[estacion]+aux


            return 0,bicicletas_en_slots,huecos_disponibles_en_slots
        elif bicicletas_en_slots[estacion] > 0:
            while bicicletas_en_slots[estacion] >0:
                bicicletas_en_slots[estacion] = bicicletas_en_slots[estacion]-1
                huecos_disponibles_en_slots[estacion]  = huecos_disponibles_en_slots[estacion] + 1
                bicicletas_input+=1

            return bicicletas_input,bicicletas_en_slots,huecos_disponibles_en_slots
        else:
            return bicicletas_input,bicicletas_en_slots,huecos_disponibles_en_slots

def estacion_cercana(estacion,bicicletas,bicicletas_en_slots,huecos_disponibles_en_slots):
    estacion_actual = estacion
    bicicletas_input = bicicletas

    indice_busqueda = 1
    estacion_encontrada = False

    estacion_siguiente = -1
    distancia_Nan = 0
    #queremos buscar una estacion cercana con posibilidad de guardar alguna bici
    if bicicletas_input > 0:
        while not estacion_encontrada:

            indice_estacion_cercana = indicesMod[estacion_actual][indice_busqueda]
            indice_estacion_cercana = int(indice_estacion_cercana)
            if huecos_disponibles_en_slots[indice_estacion_cercana] != 0:
                estacion_siguiente =  indice_estacion_cercana
                distancia_Nan = kmRelativosMod[estacion_actual][indice_busqueda]
                estacion_encontrada = True
            indice_busqueda+=1
        return bicicletas_input,estacion_siguiente, distancia_Nan
    else:
        while not estacion_encontrada:
            indice_estacion_cercana = indicesMod[estacion_actual][indice_busqueda]
            indice_estacion_cercana = int(indice_estacion_cercana)
            if bicicletas_en_slots[indice_estacion_cercana] != 0:
                estacion_siguiente =  indice_estacion_cercana
                distancia_Nan = kmRelativosMod[estacion_actual][indice_busqueda] * 3
                estacion_encontrada = True
            indice_busqueda+=1
        return bicicletas_input,estacion_siguiente, distancia_Nan
    
    
def generar_vecinos_con_offset_punto(solucion_actual, limite_vecinos, granularidad,punto_partida):
    vecinos_generados = []
    orden_numerico = np.arange(0, solucion_actual.shape[0])
    lista_permutaciones_posibles = itertools.permutations(orden_numerico, 2)
    lista_permutaciones_posibles = list(lista_permutaciones_posibles)
    # np.random.shuffle(lista_permutaciones_posibles)
    # if limite_vecinos > 240:
    #     limite_vecinos = 240

    i = punto_partida % 240


    contador = 0
    while contador < limite_vecinos:
        # print("valor contador interno ", i)
        indiceA = lista_permutaciones_posibles[i][0]
        indiceB = lista_permutaciones_posibles[i][1]
        aux = solucion_actual.copy()
        if aux[indiceA] > granularidad:
            aux[indiceA] -= granularidad
            aux[indiceB] += granularidad
            i = i + 1
            i = i % 240
            contador += 1
            vecinos_generados.append(aux)
        elif aux[indiceB] > granularidad:
            aux[indiceA] += granularidad
            aux[indiceB] -= granularidad
            i = i + 1
            i = i % 240
            contador += 1
            vecinos_generados.append(aux)
        else:
            i = i + 1
            i = i % 240
    return vecinos_generados


def inicializar_greedy(solucionInicial,limite_bicicletas):
    suma = np.array(solucionInicial).sum()
    multiplicador = limite_bicicletas/suma

    solucionInicial = np.array(solucionInicial)
    salida = solucionInicial*multiplicador

    salida = np.array(salida).round()
    return salida

def estado_inicial_random():
    random_list = np.random.uniform(0, 1, 16)

    for indice in range(16):
        suma = np.array(random_list).sum()
        #218
        multiplicador = 220 - suma
        aux = random_list[indice] * multiplicador

        if (aux > 50):
            aux = np.random.uniform(0, 50, 1)

        random_list[indice] = aux

    random_list_rounded = np.round(random_list)
    #220
    slot_random = inicializar_greedy(random_list_rounded, 220)
    return slot_random


def greedy_inicializar(dimension,limite_elementos):
    arr = np.zeros(dimension)
    for i in range(limite_elementos):
        valor = random.randint(0, dimension)
        aux = valor % dimension
        arr[aux] += 1
    return arr




def coste_slot(slot_por_estaciones):
    # Ajustamos el vector de slots al primer movimiento que tenemos que cubrir
    distanciaTotal = 0
    bicicletas_disponibles = np.zeros(slot_por_estaciones.size)
    huecos_disponibles = slot_por_estaciones - bicicletas_disponibles
    for i in range(np.array(indices).shape[1]):
        estacion = i
        bicicletas = bicicletas_objetivo_iniciales[i]
        out,bicicletas_disponibles,huecos_disponibles = (accion_posible(bicicletas, estacion,bicicletas_disponibles,huecos_disponibles))
        while out != 0:
            out, estacion_sig, distancia_aux = estacion_cercana(estacion, out,bicicletas_disponibles,huecos_disponibles)
            out, bicicletas_disponibles, huecos_disponibles = accion_posible(out, estacion_sig,bicicletas_disponibles,huecos_disponibles)

    for indice in range(np.array(lista_acciones).shape[0]):
        acc = lista_acciones[indice]
        estacion = acc[0]
        bicicletas = acc[1]
        out, bicicletas_disponibles, huecos_disponibles = accion_posible(bicicletas, estacion,bicicletas_disponibles,huecos_disponibles)
        while out != 0:
            bicis_res, estacion_sig, distancia_aux = estacion_cercana(estacion, out,bicicletas_disponibles,huecos_disponibles)
            out, bicicletas_disponibles, huecos_disponibles = (accion_posible(bicis_res, estacion_sig,bicicletas_disponibles,huecos_disponibles))
            # print("valor de out " , out , " bloqueado " , huecos_disponibles , "  " , bicicletas_disponibles)
            tmp = abs(bicis_res) - abs(out)
            distanciaTotal = distanciaTotal + distancia_aux*tmp

    return distanciaTotal




def busqueda_local(solucion_inicial):
    numero_evaluaciones = 0
    coste_minimo = math.inf

    iteraciones = 0

    slot_por_estaciones = np.array(solucion_inicial)

    # slot_por_estaciones = estado_inicial_random()
    # np.random.shuffle(slot_por_estaciones)

    bicicletas_disponibles = np.zeros(slot_por_estaciones.size)
    huecos_disponibles = slot_por_estaciones - bicicletas_disponibles
    coste_mejor = coste_slot(slot_por_estaciones)

    coste_s_inicial = coste_mejor

    no_encuentra = False
    mejora = False
    start_time = time.time()
    vecinos_totales = 240
    r = random.randint(0, 240)
    offset = r % 240

    # print("Coste inicial ", coste_slot(slot_por_estaciones))
    while not no_encuentra and iteraciones < 3000:
        lotes_size = 20
        paso = 2
        vecinos = generar_vecinos_con_offset_punto(slot_por_estaciones,lotes_size,paso,offset)
        for v in vecinos:
            aux = v.copy()
            bicicletas_disponibles = np.zeros(aux.size)
            huecos_disponibles = aux - bicicletas_disponibles
            coste_scand = coste_slot(aux)
            vecinos_totales -= 1
            mejora = False


            if coste_scand < coste_mejor:
                numero_evaluaciones += 1
                slot_por_estaciones = aux.copy()
                coste_mejor = coste_scand
                r = random.randint(0, 240)
                offset = r
                # Encuentro uno mejor reinicio el contador de vecinos de esta nueva solucion que mejora
                vecinos_totales = 240
                mejora = True


                if coste_mejor < coste_minimo:
                    coste_minimo = coste_mejor
                    mejor_slot = slot_por_estaciones.copy()


            if vecinos_totales == 0:
                # Llega al limite de vecinios establecidos para comproabr y buscar mejora, al no encontrar salimos de las comprobaciones y nos quedamos con
                # el mejor hasta el momento
                no_encuentra = True
        iteraciones+=1
        if not mejora:
            offset+= lotes_size
            mejora = False

    # print(slot_por_estaciones , "coste mejor ",coste_mejor , " " , "--- %s seconds ---" % (time.time() - start_time))
    # print(numero_evaluaciones,",")
    
    return slot_por_estaciones,coste_mejor,numero_evaluaciones


def generar_indice_ponderado_fitness(self,dimension,numero_indices_resultantes = 2):
    """
    Genera indices sobre una lista dando mayor probabilidad de seleccion a los individuos de mejor fitness
    """
    # ruleta proporcional
    
    indices_random_probabilidad = list()
    fitness = list()
    for i in range(len(self.individuos)):
        fitness.append(self.individuos[i].fitness)

    total_fitness = np.array(fitness).sum()

    fitness_individuales = list()
    for i in range(len(self.individuos)):
        fitness_individuales.append(1/(self.individuos[i].fitness / total_fitness))

    probabilidad_eleccion_norm = fitness_individuales / np.linalg.norm(fitness_individuales)

    valor_aleatorio = random.uniform(0,1)
    acumulado = 0.0
    for i in range(0,numero_indices_resultantes):
        for k in range(len(probabilidad_eleccion_norm)):
            acumulado += probabilidad_eleccion_norm[k]
            k+=1
            if(acumulado > valor_aleatorio):
                break
        indices_random_probabilidad.append(k)

    return indices_random_probabilidad
    
def calcular_indices_padres_desordenados(dimension):
    # siempre realiza los mismos cambios
    indices = np.arange(0,dimension)
    random.shuffle(indices)
    return indices


def distancia_hamming(ind_1,ind_2,diferencia_permitida= 0):
    # numero de estaciones diferentes entre padre y madre
    diff = list(abs(ind_1.contenido - ind_2.contenido))
    rep = 0
    posiciones_diferentes = []
    for k in range(0,16):
        if(diff[k] != diferencia_permitida):
            posiciones_diferentes.append(k)
    
    for i in range(0,diferencia_permitida+1):
        rep += diff.count(i)
        
    dif = 16-rep
    return dif,posiciones_diferentes

def blx_alpha_pc(padre,madre,posiciones_diferentes):
    
    dim = int(len(posiciones_diferentes)/2)
    segmento_a = posiciones_diferentes[0:dim]
    segmento_b = posiciones_diferentes[dim:(2*dim)+1]
    
    # creo una copia del padre y de la madre y a estos hijos las posiciones que eran diferentes entre padre y madre cada mitad la pasa a cada hijo
    
    # hijo formado por las estaciones quee difieren entre los padre, la mitad para cada hijo
    hijo_1 = copy.deepcopy(padre)
    for k in range(len(segmento_a)):
        indice = segmento_a[k]
        hijo_1.contenido[indice] = madre.contenido[indice].copy()
        
    
    
    # # hijo formado por madre y segmento de padre  
    hijo_2 = copy.deepcopy(madre)
    for k in range(len(segmento_b)):
        indice = segmento_b[k]
        hijo_2.contenido[indice] = padre.contenido[indice].copy()
  
    hijo_1.mutar_en_chc(segmento_diferente = segmento_a)
    hijo_2.mutar_en_chc(segmento_diferente = segmento_b)
    
    hijo_1.actualizar_individuo()
    hijo_2.actualizar_individuo()
    
    
    return hijo_1,hijo_2


def comparar_poblaciones(poblacion_anterior,poblacion):
    
    i = 0
    iguales = True
    while(i<poblacion.numero_individuos and iguales):
        iguales = np.array_equal(poblacion_anterior[i].contenido,poblacion.individuos[i].contenido) 
        i+=1
    return iguales
       


def borrar_elementos(array,indices):
        return [item for i, item in enumerate(array) if i not in indices]