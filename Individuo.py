import random
import numpy as np


import algoritmos


import algoritmosV2

class Individuo:
    """
    Clase que define nuestro concepto de individuo en nuestro problema.
    Concretamente un array con una longitud de 16 elementos, simbolizando
    cada posición el número de slot en la posición.
    
    Por defecto se genera de manera aleatoria el contenido de las estaciones.
    
    
    Parametros
    -------------
    numero_estaciones : ``int`` número de estaciones en cada individuo. (Por defecto ``16``)
    
    alpha : ``int`` valor alpha para el control del crecimiento del número de slots totales.
    
    verbose : ``bool`` muestra la información inicial del individuo en su creacion. (Por defecto ``False``)
    
    
    Atributos
    -------------
    fitness : ``float`` valor de fitness del individuo.
    contenido : ``int`` array que representa los slots de las estaciones.
    """
    
    def calculo_fitness_mod(self):
        """
        Calcula el fitness de cada individuo haciendo uso de alpha y por sobre pasar un
        número de slots total. (Por defecto ``205``)
        """
        slots_diff = abs(self.contenido.sum()-205)
        self.fitness = algoritmosV2.coste_slot(self.contenido) + self.alpha*slots_diff
    
    def __init__(self,alpha = 1.5 ,numero_estaciones = 16,verbose=False):
        
        self.numero_estaciones = numero_estaciones
        self.alpha = alpha
        # self.contenido = np.array(algoritmosV2.estado_inicial_random(),dtype=int)

        num = random.randint(205,230)
        
        self.contenido = np.array(algoritmosV2.greedy_inicializar(self.numero_estaciones,220),dtype=int)
        
        slots_diff = abs(self.contenido.sum()-205)
        self.fitness = algoritmosV2.coste_slot(self.contenido) + self.alpha*slots_diff
        self.km = self.fitness - self.alpha*slots_diff
        # self.calculo_fitness_mod()
        
        if verbose:
            print("Nuevo individuo ", self.contenido , " total slots " , self.contenido.sum(), " -- Fitness " , str(self.fitness)  , " slot diff ", self.contenido.sum()-205)
    
    
    def __repr__(self):
        return ("Individuo " + str(self.contenido)  + " total slots " + str(self.contenido.sum()) + " -- Fitness " + str(self.fitness) + " Km " +str(self.fitness-self.alpha*(self.contenido.sum()-205))  +  " slot diff "+ str(self.contenido.sum()-205)+"\n")
    
    
    def actualizar_individuo(self):
        self.contenido = self.contenido
        slots_diff = self.contenido.sum()-205
        self.fitness = algoritmosV2.coste_slot(self.contenido) + self.alpha*slots_diff
        self.km = self.fitness - self.alpha*slots_diff
        
    
    def mutar_v2(self,proba_mutacion_inf = 0.05,proba_mutacion_sup = 0.2):
        # algoritmosV2.setSemilla()
        porcentaje_mutacion = np.random.uniform(proba_mutacion_inf,proba_mutacion_sup)
        numero_mutaciones = int(np.round(self.numero_estaciones*porcentaje_mutacion))
        
        for i in range(numero_mutaciones):            
            valor = np.random.choice(np.arange(5,35))
            posicion = np.random.choice(np.arange(0,15))
            self.contenido[posicion] = valor
        
        if(self.contenido.sum() < 205):
            restante = 205-self.contenido.sum()
            self.contenido[np.random.choice(np.arange(0,15))] += restante
            
    def mutar_en_chc(self,proba_mutacion_inf = 0.05,proba_mutacion_sup = 0.2,segmento_diferente = []):
        # puede ser el valor a modificar 0, es decir, no modifico esa estacion o simepre se debe modificar
        
        
        x = np.random.normal(loc=0, scale=1, size=(len(segmento_diferente)))
        x = x.astype(int)
        for i in range(len(segmento_diferente)):
            
            if(x[i] < 0):
                valor = self.contenido[segmento_diferente[i]] + x[i]
                if( valor < 0):
                    self.contenido[segmento_diferente[i]] += (x[i]*-1)
            else:
                self.contenido[segmento_diferente[i]] += x[i]
                
            
            
        if(self.contenido.sum() < 205):
            restante = 205-self.contenido.sum()
            self.contenido[np.random.choice(np.arange(0,15))] += restante
        
    
    def mutar(self,proba_mutacion_inf = 0.05,proba_mutacion_sup = 0.2, verbose= False ):
        """
        Aplica una mutación sobre el individuo en base al porcentaje establecido.
        
        
        Parametros
        -------------
        proba_mutacion_inf : ``float`` valor % minimo a mutar del individuo.
        
        proba_mutacion_sup : ``float`` valor % maximo a mutar del individuo.
        
        verbose : ``bool`` mostrar cambios pre y post mutación. (Por defecto ``False``)
        
        """
        
        # Hay que mutar entre un 5% y 20% de cada cruze
        
        porcentaje_mutacion = np.random.uniform(proba_mutacion_inf,proba_mutacion_sup)
        numero_mutaciones = int(np.round(self.numero_estaciones*porcentaje_mutacion))
        
        # valores_modificadores = np.arange(1,numero_mutaciones+1)
        valores_modificadores = np.arange(1,10)
        np.random.shuffle(valores_modificadores)
        
        for i in range(numero_mutaciones):
            # print("numero mutaciones " , numero_mutaciones )
            a = random.choice(np.arange(0,self.numero_estaciones))
            if(np.random.uniform(0,1) > 0.5):
                # Suma valor a la estacion elegida
                if verbose:
                    print( "Posición modificada "  + str(a) + " valor sumado " + str(valores_modificadores[i]) )
                self.contenido[a] += valores_modificadores[i]
            else:
                # Resto valor a la estacion elegida
                if verbose:
                    print( "Posición modificada "  + str(a) + " valor restado " + str(valores_modificadores[i]) )
                self.contenido[a] -= valores_modificadores[i]
        
        # Aqui es donde se bloquea al calcular el fitness
        # self.calculo_fitness_mod()
        
        if verbose:
            print(self)