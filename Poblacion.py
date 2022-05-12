import random
import numpy as np
from scipy import rand
from Individuo import Individuo


import algoritmosV2

import copy

class Poblacion:
    """
    Clase que crea una población con un cierto número de individuos

    Parametros
    -------------
    numero_individuos : ``int`` número de individuos de la población.

    limite_inferior_sumatorio : ``int`` número minimo de slots para considerar al individuo válido. (Por defecto ``205``)

    verbose: ``bool`` mostrar información por pantalla. (Por defecto ``False``)

    Atributos
    -------------

    individuos : lista con todos los individuos de la población actual
    numero_individuos : ``int`` número de individuos de la población.
    limite_inferior_sumatorio : ``int`` número minimo de slots para considerar al individuo válido. (Por defecto ``205``)
    elite : lista con los 5 mejores individuos de la población actual.
    """

    def calcular_elite(self):
        sortedByFitness = sorted(self.individuos,key=lambda k: k.fitness)
        self.elite = sortedByFitness[0:5]



    def __init__(self,numero_individuos=30,alpha=1.5,limite_inferior_sumatorio=205,numero_elites=0):
        """
        Parametros
        -------------
        numero_individuos : ``int`` número de individuos de la población.

        limite_inferior_sumatorio : ``int`` número minimo de slots para considerar al individuo válido. (Por defecto ``205``)

        """
        self.numero_individuos = numero_individuos
        self.limite_inferior_sumatorio = limite_inferior_sumatorio
        # self.individuos = []
        self.individuos = np.array([])

        for i in range(self.numero_individuos):
            ind = Individuo(alpha=alpha)
            self.individuos = np.append(self.individuos,ind)
            self.individuos

        self.individuos = sorted(self.individuos,key=lambda k: k.fitness)


        self.probabilidades_progenitores = []
        self.calculo_progenitor_probabilidad()

        if(numero_elites >0):
            self.elite = []
            self.calcular_elite()


    def calculo_progenitor_probabilidad(self):
        # agregamos los indices un numero det de veces en base a su posicion
        posicion_actual = 0
        contador = self.numero_individuos
        probabilidades = []
        while(contador > 0):
            tmp = np.ones(contador)*posicion_actual
            probabilidades.extend(tmp)
            contador -= 1
            posicion_actual += 1
        probabilidades = np.array(probabilidades,dtype=int)
        self.probabilidades_progenitores = probabilidades.copy()

    def cruze_2_puntos_con_mutacion(self):

        nueva_poblacion = []
        # Generamos el numero de hijos necesarios en base al numero de individuos de la población.
        hijos = list()

        numero_hijos_validos = 0

        while(numero_hijos_validos < self.numero_individuos-len(self.elite)):
        # for indice in range(self.numero_individuos-1):

            # padre = self.individuos[random.choice(self.probabilidades_progenitores)]
            # madre = self.individuos[random.choice(self.probabilidades_progenitores)]

            indice_padre = random.choice(self.probabilidades_progenitores)
            indice_madre = random.choice(self.probabilidades_progenitores)

            padre = self.individuos[indice_padre]
            madre = self.individuos[indice_madre]



            punto_corte_a = 0
            punto_corte_b = 0
            distanciamiento = abs(punto_corte_b - punto_corte_a)
            # punto_corte_a == punto_corte_b or distanciamiento > 6:
            while distanciamiento > 8:
                punto_corte_a = random.choice(np.arange(0,15))
                punto_corte_b = random.choice(np.arange(0,15))
                distanciamiento = abs(punto_corte_b - punto_corte_a)

            if punto_corte_b < punto_corte_a:
                punto_corte_a, punto_corte_b = punto_corte_b,punto_corte_a

            # ¿ Hay que dividir el segmento para el intercambio o se intercambia el segmento completo ?
            # numero_elementos_contenidos = abs(punto_corte_b - punto_corte_a) + 1
            # if numero_elementos_contenidos % 2 == 0:

            # hijo formado por padre y segmento de madre
            hijo_1 = copy.deepcopy(padre)
            hijo_1.contenido[punto_corte_a:punto_corte_b] = madre.contenido[punto_corte_a:punto_corte_b].copy()

            # # hijo formado por madre y segmento de padre
            hijo_2 = copy.deepcopy(madre)
            hijo_2.contenido[punto_corte_a:punto_corte_b] = padre.contenido[punto_corte_a:punto_corte_b].copy()


            if(hijo_1.contenido.sum() > 205):
                # print("hijo 1")
                # hijo_1.calculo_fitness_mod()
                # slots_diff = abs(hijo_1.contenido.sum()-205)
                # hijo_1.fitness = algoritmos.coste_slot(hijo_1.contenido) + hijo_1.alpha*slots_diff
                hijo_1.mutar_v2()
                hijos.insert(numero_hijos_validos,hijo_1)
                numero_hijos_validos += 1

            if(hijo_2.contenido.sum() > 205):
                # print("hijo 2")
                # hijo_2.calculo_fitness_mod()
                # slots_diff = abs(hijo_2.contenido.sum()-205)
                # hijo_2.fitness = algoritmos.coste_slot(hijo_2.contenido) + hijo_2.alpha*slots_diff
                hijo_2.mutar_v2()
                hijos.insert(numero_hijos_validos,hijo_2)
                numero_hijos_validos += 1


        # Agregamos la elite a la nueva población.
        nueva_poblacion = copy.deepcopy(self.elite)
        nueva_poblacion = np.concatenate((nueva_poblacion,hijos[0:(self.numero_individuos-len(self.elite))]))
        nueva_poblacion = sorted(nueva_poblacion,key=lambda k: k.fitness)

        self.individuos = copy.deepcopy(nueva_poblacion)


    # def mutar_poblacion(self):

    #     nueva_poblacion = []
    #     for i in range(self.numero_individuos):
    #         ind_aux = copy.deepcopy(self.individuos[i])
    #         if ind_aux not in self.elite:
    #             ind_aux.mutar()
    #         if(np.array(ind_aux.contenido).sum() < 205):
    #             total = 205-np.array(ind_aux.contenido).sum()
    #             ind_aux.contenido[3] += total

    #         # ind_aux.fitness = algoritmos.coste_slot(ind_aux.contenido)
    #         nueva_poblacion.append(ind_aux)

    #     self.individuos = copy.deepcopy(nueva_poblacion)



    def actualizar_poblacion(self):
        for i in range(len(self.individuos)):
            self.individuos[i].contenido = self.individuos[i].contenido
            slots_diff = self.individuos[i].contenido.sum()-205
            self.individuos[i].fitness = algoritmosV2.coste_slot(self.individuos[i].contenido) + self.individuos[i].alpha*slots_diff
            self.individuos[i].km = self.individuos[i].fitness - self.individuos[i].alpha*slots_diff


    def clearing(self,kappa = 2,radio = 4):
        # modificar genetioc basico se incluye dentro del mismo este metodo
        # se aplica el multi modal indicando por parametro al GB
        nichos = []
        elementos_insertados = 0
        poblacion_tmp = copy.deepcopy(self.individuos)

        while(len(poblacion_tmp) > 0):
            # se coge siempre al inicio el primero de la poblacion
            nicho_tmp = []
            ind_cabeza = copy.deepcopy(poblacion_tmp.pop(0))
            print("individio comparacion ", ind_cabeza)
            nicho_tmp.append(ind_cabeza)
            for indice in range(0,len(poblacion_tmp)-1):
                
                distancia,seg_ = algoritmosV2.distancia_hamming(ind_cabeza,poblacion_tmp[indice])
                print("A " , ind_cabeza)
                print("B ", poblacion_tmp[indice])
                print("distancia entre ind",distancia)
                if(distancia <= radio):
                    print("Radios menor o igual")
                    if(len(nicho_tmp) < kappa):
                        print("Agrego a nicho y borro")
                        ind_dentro_radio = copy.deepcopy(poblacion_tmp.pop(indice))
                        nicho_tmp.append(ind_dentro_radio)
                    else:
                        print("Borro")
                        poblacion_tmp.pop(indice)
                    if(len(nicho_tmp) == kappa):
                        nichos.append(nicho_tmp)
                        nicho_tmp.clear()

        print("poblacion")
        print(poblacion_tmp)
        print("Nichos generados")
        print(nichos)