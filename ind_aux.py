
import algoritmos
import random
import numpy as np


class ind_aux:

    def __init__(self,alpha = 1 ,numero_estaciones = 16,verbose=False):
            
            self.numero_estaciones = numero_estaciones
            self.alpha = alpha
            
            # self.contenido = np.array(algoritmos.estado_inicial_random(),dtype=int)
            self.contenido = np.array(algoritmos.greedy_inicializar(self.numero_estaciones,220),dtype=int)
            
            slots_diff = self.contenido.sum()-205
            if slots_diff > 0 :
                self.fitness = algoritmos.coste_slot(self.contenido) + self.alpha*slots_diff
            else:
                self.fitness = algoritmos.coste_slot(self.contenido)
                
    def __repr__(self):
        return ("Individuo " + str(self.contenido)  + " total slots " + str(self.contenido.sum()) + " -- Fitness " + str(self.fitness) + " slot diff "+ str(self.contenido.sum()-205)+"\n")
    
    
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
        valores_modificadores = np.arange(1,6)
        
        for i in range(numero_mutaciones):
            pos = int(np.random.uniform(0,15))
            valor = 3
            if(np.random.uniform(0,1) > 0.7):
                self.contenido[pos] += valor
            else:
                if(self.contenido.sum() < 210):
                    self.contenido[pos] += valor
                else:
                    self.contenido[pos] -= valor
                    
            slots_diff = self.contenido.sum()-205
            if slots_diff > 0 :
                self.fitness = algoritmos.coste_slot(self.contenido) + self.alpha*slots_diff
            else:
                self.fitness = algoritmos.coste_slot(self.contenido) 
                
        
        
        
        