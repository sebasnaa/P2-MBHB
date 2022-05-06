import random
import numpy as np
from Individuo import Individuo


import algoritmos

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
        self.sortedByFitness = sorted(self.individuos,key=lambda k: k.fitness)
        self.elite = self.sortedByFitness[0:5]
   
    
    def __init__(self,numero_individuos=20,limite_inferior_sumatorio=205,verbose=False):
        
        
        self.numero_individuos = numero_individuos
        self.limite_inferior_sumatorio = limite_inferior_sumatorio
        # self.individuos = []
        self.individuos = np.array([])
        
        for i in range(self.numero_individuos):
            ind = Individuo()
            self.individuos = np.append(self.individuos,ind)
            self.individuos
        
        self.calcular_elite()
        
        # print(self.elite)
        
        print(self.sortedByFitness)
        
        
    def cruze_2_puntos(self):
        
        # Agregamos la elite a la nueva población.
        nueva_poblacion = self.elite
        
        # Generamos el numero de hijos necesarios en base al numero de individuos de la población.
        hijos = list()
        
        numero_hijos_validos = 0
        
        while(numero_hijos_validos < self.numero_individuos-5):
        
            padre = self.individuos[random.choice(np.arange(0,self.numero_individuos))]
            madre = self.individuos[random.choice(np.arange(0,self.numero_individuos))]
            
            punto_corte_a = 0
            punto_corte_b = 0
            distanciamiento = abs(punto_corte_b - punto_corte_a)
            while punto_corte_a == punto_corte_b or distanciamiento > 6:
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


            if(hijo_1.contenido.sum() > 215):
                hijo_1.calculo_fitness_mod()
                # np.append(hijos,hijo_1)
                # hijos[numero_hijos_validos] = hijo_1
                hijos.insert(numero_hijos_validos,hijo_1)
                print( "hijo 1 entra")
                numero_hijos_validos += 1
                
            if(hijo_2.contenido.sum() > 215):
                hijo_2.calculo_fitness_mod()
                # np.append(hijos,hijo_2)
                hijos.insert(numero_hijos_validos,hijo_2)
                # hijos[numero_hijos_validos] = hijo_2 
                print( "hijo 2 entra")
                numero_hijos_validos += 1
                
                
            print(numero_hijos_validos , " tamaño ")

           

        # np.append(nueva_poblacion,hijos)
        
        
        print("nueva poblacion generada ")
        print(nueva_poblacion)
        
        print("hijos creados")
        print(hijos)
        
        
        # for i in range(self.individuos.shape[0]):
        #     ind_aux = self.individuos[i]
            
        #     if ind_aux not in self.elite:
        #         nueva_poblacion.append(ind_aux)
                
        

        

        
    
   
   
    
        
   