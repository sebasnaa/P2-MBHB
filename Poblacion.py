import random
import numpy as np
import algoritmosV2
import copy

from Individuo import Individuo

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
        self.individuos = np.array([])

        for i in range(self.numero_individuos):
            ind = Individuo(alpha=alpha)
            self.individuos = np.append(self.individuos,ind)
            self.individuos

        self.individuos = sorted(self.individuos,key=lambda k: k.fitness)


        # self.probabilidades_progenitores = []
        # self.calculo_progenitor_probabilidad()

        if(numero_elites >0):
            self.elite = []
            self.calcular_elite()


    def calculo_progenitor_probabilidad(self):
        
        # agregamos los indices un numero det de veces en base a su posicion
        posicion_actual = 0
        contador = len(self.individuos)
        probabilidades = []
        while(contador > 0):
            tmp = np.ones(contador)*posicion_actual
            probabilidades.extend(tmp)
            contador -= 1
            posicion_actual += 1
        probabilidades = np.array(probabilidades,dtype=int)
        self.probabilidades_progenitores = probabilidades.copy()

    def cruce_2_puntos_con_mutacion(self,clearing=False):
        # self.calculo_progenitor_probabilidad()
        nueva_poblacion = []
        # Generamos el numero de hijos necesarios en base al numero de individuos de la población.
        hijos = list()

        numero_hijos_validos = 0

        while(numero_hijos_validos < self.numero_individuos-len(self.elite)):
            
            indices_progenitores = algoritmosV2.generar_indice_ponderado_posicion(len(self.individuos))
            
            padre = self.individuos[indices_progenitores[0]]
            madre = self.individuos[indices_progenitores[1]]

            punto_corte_a = 0
            punto_corte_b = 0
            distanciamiento = abs(punto_corte_b - punto_corte_a)
            # punto_corte_a == punto_corte_b or distanciamiento > 6:
            while distanciamiento > 6 or punto_corte_a == punto_corte_b:
                punto_corte_a = random.choice(np.arange(0,15))
                punto_corte_b = random.choice(np.arange(0,15))
                distanciamiento = abs(punto_corte_b - punto_corte_a)

            if punto_corte_b < punto_corte_a:
                punto_corte_a, punto_corte_b = punto_corte_b,punto_corte_a

          
            
            # hijo formado por padre y segmento de madre
            hijo_1 = copy.deepcopy(padre)
            if(not clearing):
                hijo_1.contenido[punto_corte_a:punto_corte_b] = madre.contenido[punto_corte_a:punto_corte_b].copy()
            else:
                if(random.uniform(0,1) < 0.8):
                    hijo_1.contenido[punto_corte_a:punto_corte_b] = madre.contenido[punto_corte_a:punto_corte_b].copy()
            # # hijo formado por madre y segmento de padre
            hijo_2 = copy.deepcopy(madre)
            if(not clearing):
                hijo_2.contenido[punto_corte_a:punto_corte_b] = padre.contenido[punto_corte_a:punto_corte_b].copy()
            else:
                if(random.uniform(0,1) < 0.8):
                    hijo_2.contenido[punto_corte_a:punto_corte_b] = padre.contenido[punto_corte_a:punto_corte_b].copy()
       
            
            
            if(hijo_1.contenido.sum() > 205):
                hijo_valido = hijo_1.mutar_v2()
                if(hijo_valido):
                    hijos.insert(numero_hijos_validos,hijo_1)
                    numero_hijos_validos += 1

            if(hijo_2.contenido.sum() > 205):
                hijo_valido = hijo_2.mutar_v2()
                if(hijo_valido):
                    hijos.insert(numero_hijos_validos,hijo_2)
                    numero_hijos_validos += 1
    
        # Agregamos la elite a la nueva población.
        nueva_poblacion = copy.deepcopy(self.elite)
        nueva_poblacion = np.concatenate((nueva_poblacion,hijos[0:(self.numero_individuos-len(self.elite))]))
        nueva_poblacion = sorted(nueva_poblacion,key=lambda k: k.fitness)

        self.individuos = copy.deepcopy(nueva_poblacion)
       


    def actualizar_poblacion(self):
        for i in range(len(self.individuos)):
            self.individuos[i].contenido = self.individuos[i].contenido
            slots_diff = self.individuos[i].contenido.sum()-205
            self.individuos[i].fitness = algoritmosV2.coste_slot(self.individuos[i].contenido) + self.individuos[i].alpha*slots_diff
            self.individuos[i].km = self.individuos[i].fitness - self.individuos[i].alpha*slots_diff

       

    

    def clearing(self,kappa = 2,radio = 4,numero_elites= 5,verbose=False):       
        nichos = []
        nichos_return = []
        pos_nicho = 0
        elementos_insertados = 1
        poblacion_tmp = copy.deepcopy(self.individuos)
        nichos = copy.deepcopy(poblacion_tmp[0:numero_elites])
        while(len(poblacion_tmp) > 0):
            if(verbose):
                print("poblacion actual size", len(poblacion_tmp))
                print(poblacion_tmp)
            nicho_tmp = []
            ind_cabeza = poblacion_tmp.pop(0)            
            if(verbose):
                print("individio seleccionado ", ind_cabeza, end="")
            nicho_tmp.append(copy.deepcopy(ind_cabeza))
            indices_agregar_en_nicho = []
            indices_borrar_poblacion = []
            for indice in range(len(poblacion_tmp)):
                
                distancia,a = algoritmosV2.distancia_hamming(ind_cabeza,poblacion_tmp[indice])
                if(verbose):
                    print("indice actual  ", indice)
                    print("A " , ind_cabeza, end="")
                    print("B ", poblacion_tmp[indice], end="")
                    print("distancia entre ind",distancia)
                if(distancia <= radio):
                    if(verbose):
                        print("Radios menor o igual,comprobamos")
                    if(elementos_insertados < kappa):
                        if(verbose):
                            print("Agrego a nicho")
                        indices_agregar_en_nicho.append(indice)
                        elementos_insertados += 1
                    else:
                        if(verbose):
                            print("Borro individuo kappa completo", end="")
                        indices_borrar_poblacion.append(indice)
            
            for i in range(len(indices_agregar_en_nicho)):
                nicho_tmp.append(copy.deepcopy(poblacion_tmp[indices_agregar_en_nicho[i]]))
                self.individuos.append(copy.deepcopy(poblacion_tmp[indices_agregar_en_nicho[i]]))
            
            indices_borrar_poblacion.extend(indices_agregar_en_nicho)
            
            poblacion_tmp = algoritmosV2.borrar_elementos(poblacion_tmp,indices_borrar_poblacion)
            elementos_insertados = 1
            nichos.extend(copy.deepcopy(nicho_tmp))
            nichos_return.insert(pos_nicho,copy.deepcopy(nicho_tmp))
            pos_nicho += 1
            nicho_tmp.clear()         
                        
        self.individuos.clear()
        self.individuos = copy.deepcopy(nichos)
        return nichos_return