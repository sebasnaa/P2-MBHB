import random
import numpy as np
from Individuo import Individuo


import algoritmos


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
        
        print(self.elite)
        
        print(self.sortedByFitness)
        
        
        
    
   
   
    
        
   