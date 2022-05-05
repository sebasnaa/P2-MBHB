import random
import numpy as np


import algoritmos

class Individuo:
    """
    Clase que define nuestro concepto de individuo en nuestro problema.
    Concretamente un array con una longitud de 16 elementos, simbolizando
    cada posición el número de slot en la posición.
    
    Por defecto se genera de manera aleatoria el contenido de las estaciones.
    
    
    Parametros
    -------------
    numero_estaciones : `int` número de estaciones en cada individuo. (Por defecto 16)
    
    verbose : `boolean` muestra la información inicial del individuo en su creacion. (Por defecto False)
    
    
    Atributos
    -------------
    fitness : `float` valor de fitness del individuo.
    contenido : `int` array que representa los slots de las estaciones.
    """
    
    
    
    def __init__(self,alpha = 1.5 ,numero_estaciones = 16,verbose=False):
        
        self.numero_estaciones = numero_estaciones
        # self.contenido = np.array(algoritmos.estado_inicial_random(),dtype=int)
        self.contenido = np.array(algoritmos.greedy_inicializar(self.numero_estaciones,220),dtype=int)
        
        slots_diff = self.contenido.sum()-205
        if slots_diff > 0 :
            self.fitness = algoritmos.coste_slot(self.contenido) + alpha*slots_diff
        else:
            self.fitness = algoritmos.coste_slot(self.contenido)
        
        
        if verbose:
            print("Nuevo individuo ", self.contenido , " total slots " , self.contenido.sum(), " -- Fitness " , str(self.fitness)  , " slot diff ", self.contenido.sum()-205)
    
    
    def __repr__(self):
        return ("Individuo " + str(self.contenido)  + " total slots " + str(self.contenido.sum()) + " -- Fitness " + str(self.fitness) + " slot diff "+ str(self.contenido.sum()-205))
    
    
    def actualizar_individuo(self):
        self.fitness = algoritmos.coste_slot(self.contenido)
    
    def mutar(self,proba_mutacion_inf = 0.05,proba_mutacion_sup = 0.2, verbose= False ):
        # Hay que mutar entre un 5% y 20% de cada cruze
        
        print(self)
        
        porcentaje_mutacion = np.random.uniform(proba_mutacion_inf,proba_mutacion_sup)
        numero_mutaciones = int(np.round(self.numero_estaciones*porcentaje_mutacion))
        
        print("num " , numero_mutaciones)
        valores_modificadores = np.arange(1,numero_mutaciones+1)
        print(valores_modificadores)
        
        for i in range(numero_mutaciones):
            a = random.choice(np.arange(0,self.numero_estaciones))
            if(np.random.uniform(0,1) > 0.5):
                # Suma valor a la estacion elegida
                print("Mut posicion "  , a , " valor sumado " , valores_modificadores[i])
                self.contenido[a] += valores_modificadores[i]
            else:
                # Resto valor a la estacion elegida
                print("Mut posicion "  , a , " valor restado " , valores_modificadores[i])
                self.contenido[a] -= valores_modificadores[i]
        
        self.actualizar_individuo()
        print("Tras mutacion")
        print(self)